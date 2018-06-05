
import os
import sys
import django
from django.db.models import Q
import time,datetime
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(BASE_DIR)
sys.path.append(BASE_DIR)
os.chdir(BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "OPcenter.settings")
django.setup()
from webmoni.models import DomainName,MonitorData

from send_warning.config import *

while True:
    # 设定轮询间隔时间
    print('开始')
    time_remaining = INTERVAL - time.time() % INTERVAL
    # 整点开始
    # time.sleep(time_remaining)
    fault_list = DomainName.objects.filter(~Q(status_id=100) & Q(check_id=0) & Q(cert_valid_days=None) & Q(warning=0))
    if len(fault_list) == 0:
        continue
    else:
        for fault in fault_list:
            start = datetime.datetime.now() - datetime.timedelta(minutes=5)
            print(fault.id)
            node_data = MonitorData.objects.filter(url_id=fault.id)
            print(node_data)