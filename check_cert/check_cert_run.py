import django
import time
import requests
from requests.exceptions import ReadTimeout
import json
from json import JSONDecodeError
import datetime
import subprocess
import ssl
import socket
from multiprocessing import Pool

from check_cert.config import *

import os
os.environ['DJANGO_SETTINGS_MODULE'] ='OPcenter.settings'
django.setup()
from webmoni.models import *



# 记录日志
def write_log(e):
    # 异常出现时间
    err_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    # 异常信息
    error_info = "[%s] %s\r\n" % (err_time, e)
    with open('error.log','a+') as f:
        f.write(error_info)

# 从 https://myssl.com/ 爬取证书信息
def getmyssl(domain_obj):
    print("getmyssl正在解析：%s" % domain_obj['url'])

    # 构建请求url,并发送请求
    url = 'https://myssl.com/api/v1/ssl_status?domain=' + domain_obj['url'] + '&port=443&c=0'
    try:
        response = requests.get(url,timeout=40)
    except ReadTimeout:
        write_log( domain_obj['url'] +  ' myssl 连接超时')
        return False

    # 挑选出证书信息的html
    CA_info_s = response.text
    try:
        CA_info_d = json.loads(CA_info_s)
    except JSONDecodeError:
        write_log(domain_obj['url'] +  ' myssl Json DecodeError')
        return False


    # 如果CA_info_doc为空,证明获取证书信息失败
    if "data" in CA_info_d:
        certs = CA_info_d['data']["status"]["certs"]
        certs["rsas"][0].get("leaf_cert_info")
        if certs["rsas"][0].get("leaf_cert_info"):
            valid_d = certs["rsas"][0].get("leaf_cert_info")
        else:
            valid_d = certs["eccs"][0].get("leaf_cert_info")
        endValid_s = valid_d["valid_to"].split("T")[0]
        endValid_l = endValid_s.split("-")
        endValid = datetime.datetime(int(endValid_l[0]), int(endValid_l[1]), int(endValid_l[2]))
        valid = endValid - datetime.datetime.today()

        return [endValid_s,valid.days]
    else:
        return False

def get_cert(domain_obj):
    try:
        ctx = ssl.create_default_context()
        s = ctx.wrap_socket(socket.socket(), server_hostname=domain_obj['url'])
        s.settimeout(5)
        s.connect((domain_obj['url'], 443))
        cert = s.getpeercert()
        # 有效期结束
        notAfter = cert['notAfter']
        notAfter = time.mktime(time.strptime(notAfter, '%b %d %H:%M:%S %Y %Z'))
        # 当前时间
        nowDate = time.time()
        # 时间差
        expire = (notAfter - nowDate) / 3600 / 24
        # 时间格式本地化
        endDate = time.strftime("%Y-%m-%d", time.localtime(notAfter))
        data = {
                'cert_valid_date': endDate,
                'cert_valid_days': int(expire)
        }
        DomainName.objects.filter(id=domain_obj['id']).update(**data)
    except Exception as e:
        write_log(e)
        result = getmyssl(domain_obj)
        if result:
            data = {
                    'cert_valid_date': result[0],
                    'cert_valid_days': int(result[1])
            }
            DomainName.objects.filter(id=domain_obj['id']).update(**data)
        else:
            data = {
                    'cert_valid_date': None,
                    'cert_valid_days': None
            }
            DomainName.objects.filter(id=domain_obj['id']).update(**data)

def sendMail(content,email):
    now_time = time.strftime("%Y-%m-%d  %H:%M:%S", time.localtime())
    try:
        result = subprocess.getstatusoutput("echo '%s' | mail -s '%s站点:%s' %s" % (content, NODE,str(now_time),email))
    except Exception as e:
        write_log(e)
        return False


if __name__ == '__main__':
    # 获取API返回的域名对象,放入检查域名的进程池检查
    domain_all = DomainName.objects.all().values()
    print(domain_all)

    # 创建进程池，进程数=THREAD_NUM，进程调用函数main，参数url_t
    try:
        pool = Pool(THREAD_NUM)
        for domain_obj in domain_all:
            if domain_obj['check_id'] == 0:
                check_number = 0
                pool.apply_async(func=get_cert, args=(domain_obj,))
        # 终止创建子进程
        pool.close()
        # 等待所有子进程结束
        pool.join()
        print('结束')
    # 进程池错误,发送邮件,写入日志,退出程序
    except Exception as e:
        sendMail(content='节点%s：进程池异常\n except:%s' % (NODE, e,), email='492960429@qq.com')
        write_log(e)
        exit()


