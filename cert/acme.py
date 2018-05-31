import subprocess
import  re
import sys,os
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
                'data':self.getcertfile()
            }

        if  re.search(r'TXT value', result[1]) is None:
            return {
                'status': 'ERROR',
                'data':result[1]
            }
        else:
            domain = re.search(r"Domain: \'(.*\.\w+)\'", result[1])
            TXT_val = re.search(r"TXT value: \'(.+)\'", result[1])
        return {
            'status': 'OK',
            'host': domain.group(1),
            'TXT':TXT_val.group(1)
        }

    def generCert(self):
        result = subprocess.getstatusoutput(
            self.acme + ' --renew  -d ' + self.domain + ' --yes-I-know-dns-manual-mode-enough-go-ahead-please')
        if re.search(r'Cert success.',result[1]) is not None:
            return True
        else:
            return result[1]

    def getcertfile(self):
        files = os.listdir(self.basedir+self.domain)
        return files


    def cert_download(self,file_path):
        file = self.basedir + file_path
        return str(file)

    def getcertdir(self):
        result = subprocess.getstatusoutput(self.acme + " --list | awk '{print $1}' |tail -n +2")
        cert_dir = result[1].split('\n')
        return cert_dir






content = '''
[2018年 05月 28日 星期一 14:44:04 CST] Single domain='limlin.cn'
[2018年 05月 28日 星期一 14:44:04 CST] Getting domain auth token for each domain
[2018年 05月 28日 星期一 14:44:04 CST] Getting webroot for domain='limlin.cn'
[2018年 05月 28日 星期一 14:44:04 CST] Getting new-authz for domain='limlin.cn'
[2018年 05月 28日 星期一 14:44:24 CST] The new-authz request is ok.
[2018年 05月 28日 星期一 14:44:24 CST] Add the following TXT record:
[2018年 05月 28日 星期一 14:44:24 CST] Domain: '_acme-challenge.limlin.cn'
[2018年 05月 28日 星期一 14:44:24 CST] TXT value: 'M7pMrtTF-88Z7EbFiduUfoUQVecaSn7uzNyXikUub8s'
[2018年 05月 28日 星期一 14:44:24 CST] Please be aware that you prepend _acme-challenge. before your domain
[2018年 05月 28日 星期一 14:44:24 CST] so the resulting subdomain will be: _acme-challenge.limlin.cn
[2018年 05月 28日 星期一 14:44:24 CST] Please add the TXT records to the domains, and re-run with --renew.
[2018年 05月 28日 星期一 14:44:24 CST] Please check log file for more details: /root/.acme.sh/acme.sh.log
'''

content1 = '''(1, '[2018年 05月 28日 星期一 13:45:46 CST] Creating domain key\n[2018年 05月 28日 星期一 13:45:46 CST] The domain key is here: /root/.acme.sh/baidu.com/baidu.com.key\n[2018年 05月 28日 星期一 13:45:46 CST] Single domain=\'baidu.com\'\n[2018年 05月 28日 星期一 13:45:46 CST] Getting domain auth token for each domain\n[2018年 05月 28日 星期一 13:45:46 CST] Getting webroot for domain=\'baidu.com\'\n[2018年 05月 28日 星期一 13:45:46 CST] Getting new-authz for domain=\'baidu.com\'\n[2018年 05月 28日 星期一 13:45:51 CST] The new-authz request is ok.\n[2018年 05月 28日 星期一 13:45:51 CST] new-authz error: {"type":"urn:acme:error:rejectedIdentifier","detail":"Error creating new authz :: Policy forbids issuing for name","status": 400}\n[2018年 05月 28日 星期一 13:45:51 CST] Please check log file for more details: /root/.acme.sh/acme.sh.log')
'''

