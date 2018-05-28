import subprocess
import  re


d = 'limlin.cn'

class ACME_cll(object):
    def __init__(self,domain):
        self.domain = domain
        self.acme = '/root/.acme.sh/acme.sh'


    def generTXT(self):
        result = subprocess.getstatusoutput(self.acme + ' --issue  --dns -d ' + self.domain  + ' --yes-I-know-dns-manual-mode-enough-go-ahead-please')
        if  re.search(r'TXT value', result) is None:
            return {
                'status': 'ERROR',
                'data':result[1]
            }
        else:
            domain = re.search(r"Domain: \'(.*\.\w+)\'", result[1])
            TXT_val = re.search(r"TXT value: \'(.+)\'", result[1])
        return {
            'status': 'OK',
            'host': domain,
            'TXT':TXT_val
        }

    def generCert(self):
        result = subprocess.getstatusoutput(
            self.acme + ' --renew  -d ' + self.domain + ' --yes-I-know-dns-manual-mode-enough-go-ahead-please')

        return result

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

result = re.search(r'TXT value',content)
if result is None:
    print(result)