import ssl
import socket
import time,datetime
import requests
from requests.exceptions import ReadTimeout
import json
import re
import random
from json import JSONDecodeError
from pyquery import PyQuery as pq
import django
import os,sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.chdir(BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "OPcenter.settings")
django.setup()
from webmoni.models import DomainName

class Cert_check(object):
    def __init__(self,domain):
        self.domain = domain
        self.sslchaoshi = 'https://api-tools.sslchaoshi.com/ssltools/sslVerity'
        self.myssl = 'https://myssl.com/api/v1/ssl_status?domain=' + self.domain + '&port=443&c=0'
        self.data = {
            'endDate':None,
            'expire':None
        }
        self.func_list = [self.getmyssl,self.getChacuoPage,self.getsslchaoshi]


    def py_check(self):
        try:
            ctx = ssl.create_default_context()
            s = ctx.wrap_socket(socket.socket(), server_hostname=self.domain)
            s.settimeout(5)
            s.connect((self.domain, 443))
            cert = s.getpeercert()
            # 有效期结束
            notAfter = time.mktime(time.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z'))
            # 当前时间
            nowDate = time.time()
            # 时间差
            self.data['expire'] = int((notAfter - nowDate) / 3600 / 24)
            # 时间格式本地化
            self.data['endDate'] = time.strftime("%Y-%m-%d", time.localtime(notAfter))
            # print(self.domain,self.data)
            return self.data
        # except socket.gaierror as e:
        #     print(self.domain,e)
        # except socket.timeout as e:
        #     print(self.domain,e)
        # except ssl.SSLError as e:
        #     print(self.domain,e)
        # except ssl.CertificateError as e:
        #     print(self.domain,e)
        except Exception:
            for i in range(0,len(self.func_list)):
                func = self.func_list.pop(random.randint(0,len(self.func_list)-1))
                result = func()
                if result:
                    return result
            return self.data


    # 从 https://myssl.com/ 爬取证书信息
    def getmyssl(self):
        print("getmyssl正在解析：%s" % self.domain)

        # 构建请求url,并发送请求
        url = 'https://myssl.com/api/v1/ssl_status?domain=' + self.domain + '&port=443&c=0'
        try:
            response = requests.get(url, timeout=20)
        except Exception:
            return False

        # 挑选出证书信息的html
        try:
            CA_info_d = json.loads(response.text)
        except JSONDecodeError:
            return False

        # 如果CA_info_doc为空,证明获取证书信息失败
        if "data" in CA_info_d:
            try:
                valid_d = CA_info_d['data']["status"]["certs"]["rsas"][0]["leaf_cert_info"]
            except IndexError:
                valid_d = CA_info_d['data']["status"]["certs"]["eccs"][0]["leaf_cert_info"]
                return False
            except KeyError:
                return False

            endValid_s = valid_d["valid_to"].split("T")[0]
            endValid_l = endValid_s.split("-")
            endValid = datetime.datetime(int(endValid_l[0]), int(endValid_l[1]), int(endValid_l[2]))
            valid = endValid - datetime.datetime.today()
            self.data['endDate'] = endValid_s
            self.data['expire'] = valid.days
            return self.data
        else:
            return False


    def getsslchaoshi(self):
        print("sslchaoshi正在解析：%s" % self.domain)

        # 设置请求url和需要POST的数据,并发送POST请求,会返回一个字典
        url = "https://api-tools.sslchaoshi.com/ssltools/sslVerity"
        data = {'hostname': self.domain, "port": 443}
        try:
            response = requests.post(url, data, timeout=20)
        except Exception:
            return False

        ssl_data = json.loads(response.text)

        # 如果有cerInfo这个key,说明获取证书信息成功,
        if "cerInfo" in ssl_data:
            # 获取证书信息成功,构建正确证书信息字典,并存入mongoDB
            to = ssl_data["cerInfo"]['activeTimeStamp']["to"]
            restTime = ssl_data["cerInfo"]['activeTimeStamp']["restTime"]
            self.data['endDate'] = time.strftime("%Y-%m-%d", time.localtime(to))
            self.data['expire'] = int(re.sub(r"天", "", restTime))

            return self.data
        else:
            return False

    # 从 http://web.chacuo.net/netsslcheck 爬去证书信息
    def getChacuoPage(self):
        print("chacuo正在解析：%s" % self.domain)

        # 拼接url
        # domain是需要检测的域名
        url = "http://web.chacuo.net/netsslcheck?type=sslcheck&data=" + self.domain

        # 发送请求
        try:
            response = requests.get(url, timeout=20)
        except Exception:
            return False


        # 将返回内容转换为字典,如果出现JSONDecodeError就从新调用当前函数再请求一次
        try:
            data = json.loads(response.text)
        except JSONDecodeError:
            return False

        # 如果返回的字典里的data这个key没有值,说明获取证书信息失败,
        if len(data["data"][0]) == 0:
            return False
        domainInfo_list = []
        # 解析数据,将有值的数据追加到domainInfo_list中
        doc = pq(data['data'][0])
        for i in doc("tr").items():
            info = i.text().split("\n")
            if len(info) == 2:
                domainInfo_list.append(info)

        # 将domainInfo_list转换为字典,并插入domain字段,保存到mongodb中
        detail = dict(domainInfo_list)
        self.data['endDate'] = detail['有效时间：'].split("到")[1]
        self.data['expire'] = int(re.search(r"\d+", detail['过期时间：：']).group())
        return self.data




if __name__ == '__main__':
    domain_all = DomainName.objects.all()
    print(domain_all)
    for domain_obj in domain_all:
        if domain_obj.check_id == 0:
            obj = Cert_check(domain_obj.url)
            data = obj.py_check()
            domain_obj.cert_valid_date = data['endDate']
            domain_obj.cert_valid_days = data['expire']
            domain_obj.save()