
import os
import sys
import django
from django.db.models import Q
import time,datetime
import subprocess
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(BASE_DIR)
sys.path.append(BASE_DIR)
os.chdir(BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "OPcenter.settings")
django.setup()
from webmoni.models import DomainName,MonitorData,Node
from send_warning.config import *
from OPcenter.settings import webmoni_error_trigger

while True:
    # 设定轮询间隔时间
    time_remaining = INTERVAL - time.time() % INTERVAL
    # 整点开始
    time.sleep(time_remaining)
    fault_list = DomainName.objects.filter(~Q(status_id=100) & Q(check_id=0) & Q(warning=0))
    if len(fault_list) == 0:
        continue
    else:
        for fault in fault_list:
            start = datetime.datetime.now() - datetime.timedelta(minutes=5)
            node_data = MonitorData.objects.filter(Q(url_id=fault.id) & Q(datetime__gt=start) & ~Q(total_time=None))
            if node_data.count() < webmoni_error_trigger:
                shanghai = None if node_data.filter(node_id=3).first() is None else node_data.filter(node_id=3).first().total_time
                beijing = None if node_data.filter(node_id=6).first() is None else node_data.filter(node_id=6).first().total_time
                qingdao = None if node_data.filter(node_id=4).first() is None else node_data.filter(node_id=4).first().total_time
                shenzhen = None if node_data.filter(node_id=5).first() is None else node_data.filter(node_id=5).first().total_time
                content = '''域名：%s 
项目：%s 
上海：%s/ms 
北京：%s/ms
青岛：%s/ms 
深圳：%s/ms
证书状态：%s天 
时间：%s ''' %(fault.url,fault.project_name,shanghai,beijing,qingdao,shenzhen,fault.cert_valid_days,time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
                subprocess.getstatusoutput("echo '%s' | mail -s '域名提醒:%s' 492960429@qq.com" %(content,fault.url))
                subprocess.getstatusoutput("echo '%s' | mail -s '域名提醒:%s' epay7777@gmail.com" %(content,fault.url))
