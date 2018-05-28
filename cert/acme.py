import subprocess
import  re


d = 'limlin.cn'

class ACME_cll(object):
    def __init__(self,domain):
        self.domain = domain
        self.acme = '/root/.acme.sh/acme.sh'


    def generTXT(self):
        result = subprocess.getstatusoutput(self.acme + ' --issue  --dns -d ' + self.domain  + ' --yes-I-know-dns-manual-mode-enough-go-ahead-please')
        domain = re.search(r"Domain: \'(.*\.\w+)\'", result[1])
        TXT_val = re.search(r"TXT value: \'(.+)\'", result[1])
        return {
            'host':domain.group(1),
            'TXT':TXT_val.group(1)
        }

    def generCert(self):
        result = subprocess.getstatusoutput(
            self.acme + ' --renew  -d ' + self.domain + ' --yes-I-know-dns-manual-mode-enough-go-ahead-please')

        return result

    