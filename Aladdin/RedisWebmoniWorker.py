import django
import os,sys
import time
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.chdir(BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "OPcenter.settings")
django.setup()
from django.conf import settings
redis_id = settings.REDIS_IP
redis_password = settings.REDIS_PASSWORD

from Aladdin.CheckCertModule import Cert_check
from webmoni.models import DomainName,Node

from Aladdin.RedisQueue import Redis_Queue
from Aladdin.EMailModule import send_mail
from Aladdin.config import Webmoni_Check_Cert_Queue,Webmoni_Send_Mail_Queue,NodeTriggerNumber,Benz,Ming,Lin


# 检查证书
class Check_Cert_Worker(object):
    def __init__(self):
        # 存储检查过的域名最近一次检查时间
        self.worker = Redis_Queue(Webmoni_Check_Cert_Queue)
        self.radio = self.worker.subscribe()

    def start(self):
        """
        收听来自webmoni_check_cert频道的节目
        :return:
        """
        print('Check Cert Worker 已启动')
        while True:
            msg = self.radio.parse_response()
            program = eval(msg[2].decode())
            pattern = program.get('pattern')
            if pattern == 0: # 节目模式=0 就检测所有域名
                domain_list = DomainName.objects.filter(check_id=0).values('url')
                for row in domain_list:
                    domain = row.get('url')
                    c = Cert_check(domain)
                    cert_info = c.py_check()
                    DomainName.objects.filter(url=domain).update(cert_valid_date=cert_info['endDate'],
                                                             cert_valid_days=cert_info['expire'])
            elif pattern == 1:  # 节目模式=1 检测单个域名
                domain = program.get('domain')
                c = Cert_check(domain)
                cert_info = c.py_check()
                DomainName.objects.filter(url=domain).update(cert_valid_date=cert_info['endDate'],
                                                         cert_valid_days=cert_info['expire'])



class Send_Mail_Worker(object):
    def __init__(self):
        self.cache = {'current':0,'data':{}}
        self.worker = Redis_Queue(Webmoni_Send_Mail_Queue)
        self.radio = self.worker.subscribe()

    def start(self):
        print('Send Mail Worker 已启动')
        while True:
            msg = self.radio.parse_response()
            program = eval(msg[2].decode())
            current = program.get('time') - program.get('time') % 300
            status = program.get('status')
            url_id = program.get('url_id')
            if current == self.cache.get('current') :
                if not self.cache['data'].get(program['domain']):
                    self.cache['data'][program['domain']] = {'failtag':0,'areas':{}}
                    if not status == 100:
                        self.cache['data'][program['domain']]['failtag'] = 1
                else:
                    if not status == 100:
                        self.cache['data'][program['domain']]['failtag'] += 1
                self.cache['data'][program['domain']]['areas'][str(program.get('node'))] = program.get('total_time')

            else:
                node_info = {}
                for node in Node.objects.all():
                    node_info[str(node.id)] = node.node
                self.cache['current'] = current
                if self.cache.get('data') is None:
                    continue
                for domain,y in self.cache['data'].items():
                    print(int(len(y['areas']) / 2) + 1)
                    if y['failtag'] >= int(len(y['areas']) / 2) + 1:
                        DomainName.objects.filter(url=domain).update(status=99)
                        content = '域名:{}<br>'.format(domain,domain)
                        for area,val in y['areas'].items():
                            content += '{}:{}<br>'.format(node_info[area],val)
                            print(content)
                        content += '<a href="http://139.199.77.249:8000/webmoni/Nowarning/{}/">点击不警告</a><br>'.format(domain)
                        send_mail(domain,[Ming,Lin],content)
                    else:
                        DomainName.objects.filter(url=domain).update(status=100)
                self.cache['data'].clear()





