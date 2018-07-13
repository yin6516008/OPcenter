import threading
import os,sys
import django
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.chdir(BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "OPcenter.settings")
django.setup()

from Aladdin.RedisWebmoniWorker import Send_Mail_Worker,Check_Cert_Worker
from Aladdin.RedisSaltWorker import Minion_Check_Worker,Minion_Auto_Check_Worker



if __name__ == '__main__':
    worker_list = [
        Send_Mail_Worker,
        Check_Cert_Worker,
        Minion_Check_Worker,
        Minion_Auto_Check_Worker,
    ]
    for worker in worker_list:
        w = worker()
        t = threading.Thread(target=w.start,)
        t.start()