import subprocess
import  re
import sys,os,json
import shutil
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
        print(type(excode))
        result = subprocess.getstatusoutput(excode)
        print(result)
        if re.search(r'Cert success.', result[1]) is not None:
            return {
                'status':'SUCCESS',
                'data':self.getcertfile(),
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
            TXT_val = re.search(r"TXT value: \'(.+)\'", result[1])
        return {
            'status': 'OK',
            'host': domain.group(1),
            'TXT':TXT_val.group(1),
            'sys_info':result[1]
        }

    def generCert(self):
        result = subprocess.getstatusoutput(
            self.acme + ' --renew  -d ' + self.domain + ' --yes-I-know-dns-manual-mode-enough-go-ahead-please')
        if re.search(r'Cert success.',result[1]) is not None:
            files = self.getcertfile()
            return {
              'status':'OK',
              'files':files,
              'sys_info':result[1]
            }
        else:
            files = self.getcertfile()
            return {
                'status': 'ERROR',
                'files': files,
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
        cert_dir = result[1].split('\n')
        return cert_dir

    def cert_delete(self):
        cert_abs_path = self.basedir + self.domain
        if os.path.exists(cert_abs_path):
            shutil.rmtree(cert_abs_path)
            return True
        else:
            return False
