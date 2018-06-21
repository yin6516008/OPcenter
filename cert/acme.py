import subprocess
import  re
import sys,os,json
import shutil
import time
import zipfile
from django.http import HttpResponse
d = 'limlin.cn'

class ACME_cll(object):
    def __init__(self,domain=None):
        self.domain = domain
        self.basedir = '/root/.acme.sh/'
        self.acme = '/root/.acme.sh/acme.sh'


    def generTXT(self):
        # cert_dir = self.basedir + self.domain
        # if os.path.exists(cert_dir):shutil.rmtree(cert_dir)
        excode = self.acme + ' --issue  --dns -d ' + self.domain  + ' --yes-I-know-dns-manual-mode-enough-go-ahead-please'
        result = subprocess.getstatusoutput(excode)
        if re.search(r'Cert success.', result[1]) is not None:
            self.zip_cert()
            return {
                'status':'SUCCESS',
                'files':self.getcertfile(),
                'sys_info':result[1]
            }

        if  re.search(r'TXT value', result[1]) is None:
            return {
                'status': 'ERROR',
                'data':result[1],
                'sys_info':result[1]
            }
        else:
            domain = re.search(r"Domain: \'(.*\.\w+)\'", result[1])
            host_list = domain.group(1).split('.')[0:-2]
            host = '.'.join(host_list)
            TXT_val = re.search(r"TXT value: \'(.+)\'", result[1])
        return {
            'status': 'OK',
            'host': host,
            'TXT':TXT_val.group(1),
            'sys_info':result[1]
        }

    def generCert(self):
        result = subprocess.getstatusoutput(
            self.acme + ' --renew  -d ' + self.domain + ' --yes-I-know-dns-manual-mode-enough-go-ahead-please')
        if re.search(r'Cert success.',result[1]) is not None:
            self.zip_cert()
            return {
              'status':'OK',
              'sys_info':result[1]
            }
        else:
            return {
                'status': 'ERROR',
                'sys_info':result[1]
            }

    def getcertfile(self):
        files = os.listdir(self.basedir+self.domain)
        return files


    def cert_download(self,file_path):
        file = self.basedir + file_path
        return str(file)

    def getcertdir(self):
        result = subprocess.getstatusoutput(self.acme + " --list |tail -n +2")
        if result[1] == '':
            return None
        else:
            cert_dir = result[1].split('\n')
            return cert_dir



    def cert_delete(self):
        cert_abs_path = self.basedir + self.domain
        if os.path.exists(cert_abs_path):
            shutil.rmtree(cert_abs_path)
            return True
        else:
            return False

    def zip_cert(self):
        domain_path = self.basedir + self.domain + '/'
        cer = domain_path + self.domain+ '.cer'
        key = domain_path + self.domain+ '.key'
        pfx = domain_path + self.domain+ '.pfx'
        pem = domain_path + self.domain+ '.pem'
        password_file = domain_path + 'password-' +self.domain + '.txt'

        iis_zip = domain_path + 'iis-' + self.domain + '.zip'
        nginx_zip = domain_path +'nginx-' + self.domain + '.zip'

        password = str(int(time.time()))

        result = subprocess.getstatusoutput('openssl x509 -in '+cer+' -out '+pem+' -outform pem')
        result = subprocess.getstatusoutput('openssl pkcs12 -export -in '+cer+' -inkey '+key+' -out '+pfx+' -certfile '+cer+' -password pass:'+password)
        with open(password_file,'w+') as f:
            f.write(password)

        # 打开或新建压缩文件
        iis_zp = zipfile.ZipFile(iis_zip, 'w', zipfile.ZIP_DEFLATED)  # 设置zipfile.ZIP_DEFLATED参数,压缩后的文件大小减小
        # 向压缩文件中添加文件内容
        iis_zp.write(pfx,os.path.basename(pfx))
        iis_zp.write(password_file,os.path.basename(password_file))
        iis_zp.write(pem,os.path.basename(pem))
        iis_zp.write(key,os.path.basename(key))
        # 关闭压缩文件对象
        iis_zp.close()

        # 打开或新建压缩文件
        nginx_zp = zipfile.ZipFile(nginx_zip, 'w', zipfile.ZIP_DEFLATED)  # 设置zipfile.ZIP_DEFLATED参数,压缩后的文件大小减小
        # 向压缩文件中添加文件内容
        nginx_zp.write(pem,os.path.basename(pem))
        nginx_zp.write(key,os.path.basename(key))
        # 关闭压缩文件对象
        nginx_zp.close()




