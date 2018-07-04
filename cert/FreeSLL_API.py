import requests
import json
import redis
import time
import subprocess
import zipfile
import os


class TrustAsia(object):
    def __init__(self):
        self.account = "mingdeop@sina.com"
        self.password = "Kemingjunde888"
        self.headers = {
                            "user-agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36",
                            'Accept-Language':'zh-CN,zh;q=0.9'
                        }
        self.redis = redis.Redis(host='139.199.77.249', password="Kemingjunde888", port=6379,db=0)
        self.basedir = "/root/.acme/TrustAsia/"

    def login(self):
        data = {
            "email":self.account,
            "password":self.password
        }

        response = requests.post("https://freessl.org/api/login",headers=self.headers,data=data)
        return_value = json.loads(response.text)
        if return_value.get("code") == 0:
            self.redis.set("OPcent_cookies",response.cookies.get_dict())
            return True
        else:
            return return_value

    def Order_list(self,):
        OPcent_cookies = eval(self.redis.get("OPcent_cookies"))
        response = requests.get("https://freessl.org/api/orders?pagesize=1000&page=1",headers=self.headers,cookies=OPcent_cookies)
        return_value = json.loads(response.text)
        return return_value

    def Orders_detail(self,order_id):
        OPcent_cookies = eval(self.redis.get("OPcent_cookies"))
        response = requests.get("https://freessl.org/api/orders/detail/" + order_id,headers=self.headers,cookies=OPcent_cookies)
        return_value = json.loads(response.text)
        return return_value


    def Order_delete(self,order_id,status):
        OPcent_cookies = eval(self.redis.get("OPcent_cookies"))

        if status == "4":
            print(order_id, status)
            data = {
                "password":self.password
            }
            response = requests.post("https://freessl.org/api/orders/delete/"+order_id,headers=self.headers,cookies=OPcent_cookies,data=data)
            return_value = json.loads(response.text)
            return return_value
        else:

            response = requests.post("https://freessl.org/api/orders/delete/"+order_id,headers=self.headers,cookies=OPcent_cookies)
            return_value = json.loads(response.text)
            return return_value


    def Cert_list(self):
        data = {
            "page": 1,
            "pagesize": 10
        }
        OPcent_cookies = eval(self.redis.get("OPcent_cookies"))
        response = requests.get("https://freessl.org/api/certs?page=1&pagesize=1000&search=&target=", headers=self.headers,data=data,
                                 cookies=OPcent_cookies)
        return_value = json.loads(response.text)
        return return_value

    def Create_order(self,domain,algorithm):
        OPcent_cookies = eval(self.redis.get("OPcent_cookies"))
        data = {
            "email": "mingdeop@sina.com",
            "authmethod": "dns",
            "keytype": algorithm,
            "domains":domain,
            "brand":"trustasia",
            "csrpem":"",
            "from":""
        }
        response = requests.post("https://freessl.org/api/order/create",headers=self.headers,data=data,cookies=OPcent_cookies)
        return_value = json.loads(response.text)
        return return_value


    def Order_Authz(self,domain,order):
        OPcent_cookies = eval(self.redis.get("OPcent_cookies"))
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36",
            'Accept-Language': 'zh-CN,zh;q=0.9',
            "authority": "freessl.org",
            "method": "GET",
            "path": "/api/order/authz/DOstvcya19958?brand = trustasia",
            "scheme": "https",
            "referer": "https://freessl.org/dashboard/orderlist"
        }

        verify_url = "https://freessl.org/api/order/authz/"+order+"?brand=trustasia"
        response = requests.get(verify_url, headers=headers,cookies=OPcent_cookies)
        verify_return_value = json.loads(response.text)
        if verify_return_value.get("code") == 0:
            download_cert_url = "https://freessl.org/api/order/cert/"+order+"?brand=trustasia"
            download_return_value = requests.get(download_cert_url, headers=headers, cookies=OPcent_cookies)
            auth_info = json.loads(download_return_value.text)
            cert_key = auth_info["msg"]
            if not os.path.exists(self.basedir):
                os.makedirs(self.basedir)
            domaindir = self.basedir + domain + "/"
            if not os.path.exists(domaindir):
                os.makedirs(domaindir)
            pem = domaindir + domain +".pem"
            CA_cert = domaindir +domain +".cer"
            key = domaindir + domain +".key"
            pfx = domaindir + domain +'.pfx'

            iis_zip =  domaindir + 'iis-' + domain +'.zip'
            nginx_zip = domaindir + 'nginx-' + domain +'.zip'

            password_file = domaindir + 'password-' + domain + '.txt'

            with open(pem,"w") as f:
                f.write(cert_key["cert"])

            with open(CA_cert,"w") as pf:
                pf.write(cert_key["cacert"])

            with open(key,"w") as k:
                k.write(cert_key["key"])

            password = str(int(time.time()))
            with open(password_file,"w") as p:
                p.write(password)

            result = subprocess.getstatusoutput(
                'openssl pkcs12 -export -in ' + pem + ' -inkey ' + key + ' -out ' + pfx + ' -certfile ' + CA_cert + ' -password pass:' + password)


            # 打开或新建压缩文件
            iis_zp = zipfile.ZipFile(iis_zip, 'w', zipfile.ZIP_DEFLATED)  # 设置zipfile.ZIP_DEFLATED参数,压缩后的文件大小减小
            # 向压缩文件中添加文件内容
            iis_zp.write(pfx, os.path.basename(pfx))
            iis_zp.write(password_file, os.path.basename(password_file))
            iis_zp.write(pem, os.path.basename(pem))
            iis_zp.write(key, os.path.basename(key))
            # 关闭压缩文件对象
            iis_zp.close()

            # 打开或新建压缩文件
            nginx_zp = zipfile.ZipFile(nginx_zip, 'w', zipfile.ZIP_DEFLATED)  # 设置zipfile.ZIP_DEFLATED参数,压缩后的文件大小减小
            # 向压缩文件中添加文件内容
            nginx_zp.write(pem, os.path.basename(pem))
            nginx_zp.write(key, os.path.basename(key))
            # 关闭压缩文件对象
            nginx_zp.close()

            return auth_info
        else:
            return verify_return_value

    def Cert_delete(self,sha1):
        OPcent_cookies = eval(self.redis.get("OPcent_cookies"))
        data = {
                "password":self.password
            }
        response = requests.post("https://freessl.org/api/certs/delete/"+sha1,headers=self.headers,cookies=OPcent_cookies,data=data)
        return_value = json.loads(response.text)
        return return_value


    def Cert_nginx_download(self,domain):
        return self.basedir + domain +"/"+ 'nginx-' + domain +'.zip'

    def Cert_iis_download(self,domain):
        return self.basedir + domain +"/"+ 'iis-' + domain +'.zip'

    def Cert_detail(self,sha1):
        OPcent_cookies = eval(self.redis.get("OPcent_cookies"))
        response = requests.get("https://freessl.org/api/certs/detail/"+sha1, headers=self.headers,
                                 cookies=OPcent_cookies)
        return_value = json.loads(response.text)
        return return_value

    def Cert_select(self,order_id):
        OPcent_cookies = eval(self.redis.get("OPcent_cookies"))
        sha1_response = requests.get("https://freessl.org/api/orders/cert/" + order_id, headers=self.headers,
                                cookies=OPcent_cookies)
        print(sha1_response.text)
        sha1_return_value = json.loads(sha1_response.text)
        if sha1_return_value.get("code") == 0:
            response = requests.get("https://freessl.org/api/certs?page=1&pagesize=10&search=sha1&target="+sha1_return_value["msg"]["sha1"], headers=self.headers,
                                         cookies=OPcent_cookies)
            return_value = json.loads(response.text)
            return return_value
        else:
            return sha1_return_value

