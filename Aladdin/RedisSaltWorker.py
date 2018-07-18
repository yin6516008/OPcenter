from redis import Redis
import django
import os,sys,time
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.chdir(BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "OPcenter.settings")
django.setup()
from django.conf import settings
from saltstack.salt_manage import Test_ping,Grains,Minion_state
from saltstack.models import Accepted_minion
from salt import client

redis_id = settings.REDIS_IP
redis_password = settings.REDIS_PASSWORD
from Aladdin.RedisQueue import Redis_Queue


# redis接收消息
class Minion_Check_Worker(object):
    def __init__(self):

        self.worker = Redis_Queue('check_minion')
        self.radio = self.worker.subscribe()

    # 检测主机队列
    def start(self):
        print('Minion Check Worker 已启动')
        while True:
            # 接收队列消息
            msg = self.radio.parse_response()
            # 解析消息内容
            msg = eval(msg[2])
            time.sleep(10) if msg['add'] else None
            # 调用test.ping测试
            minion_check = Test_ping()
            # 检测主机配置
            grains = Grains()
            if msg['pattern'] == 1: # 检测主机
                minion_check.get_status(msg['id'])
            if msg['pattern'] == 2: # 获取主机信息
                grains.get_minion_items(msg['id'])

class Minion_Auto_Check_Worker(object):
    def __init__(self):
        self.worker = Redis_Queue('check_minion')
    def start(self):
        print('Minion Auto Check Worker 已启动')
        while True:
            # 设定自动检测间隔时间
            time.sleep(600)
            minion_id_dict = Accepted_minion.objects.values('id')
            minion_id_list = []
            for minion_id in minion_id_dict:
                minion_id_list.append(minion_id['id'])
            time.sleep(1)
            # 定时发送检测任务到redis队列
            test = {'pattern': 1,'id':minion_id_list,'add':False}
            self.worker.publish(test)

class Execute_PlayBook_Worker(object):
    def __init__(self):
        self.worker = Redis_Queue('state_execute')
        self.radio = self.worker.subscribe()
        self.client = client.LocalClient()
    def start(self):
        print('Execute PlayBook Worker 已启动')
        while True:
            # 接收队列消息
            msg = self.radio.parse_response()
            # 解析消息内容
            msg = eval(msg[2])
            print('state_execute频道接收消息：', msg)
            # 执行状态
            minion_state = Minion_state()
            result = minion_state.exe_sls(msg['number'],msg['minion_id_list'], msg['playbook_id'])
            print(result)
            jid = result[0]
            number = result[1]
            t = 1
            # 判断异常
            if jid not in msg['minion_id_list'] and type(jid) == int and jid > 0:
                # 持续查询，直到出现结果，或者连接超时
                while not self.client.get_cache_returns(jid):
                    time.sleep(1)
                    if t == 600:
                        information = {'ERROR':'Timeout'}
                        break
                    else:
                        t += 1
                else:
                    information = self.client.get_cache_returns(jid)
                # 继续查询，直到全部主机执行结果全部得到
                if len(information) != len(msg['minion_id_list']):
                    while len(self.client.get_cache_returns(jid)) != len(msg['minion_id_list']):
                        time.sleep(1)
                        if t == 600:
                            information = {'ERROR':'Timeout'}
                            break
                        else:
                            t += 1
                    else:
                        information = self.client.get_cache_returns(jid)
                minion_state.save_sls(number=number,information=information,status=2)
                print('任务完成，state_execute频道继续接收消息')
            else:
                information = {'ERROR':'未选择主机或剧本'} if jid == 0 else {'不存在的主机':result[0]}
                minion_state.save_sls(number=number, information=information,status=3)
                print('任务异常，state_execute频道继续接收消息')
                continue
                # 继续订阅

# if __name__=='__main__':
#     exe_state = Execute_PlayBook_Worker()
#     exe_state.start()