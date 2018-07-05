from redis import Redis
import django
import os,sys,time
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.chdir(BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "OPcenter.settings")
django.setup()
from django.conf import settings
from saltstack.salt_manage import Test_ping,Grains,State_sls


redis_id = settings.REDIS_IP
redis_password = settings.REDIS_PASSWORD
from Aladdin.RedisQueue import Redis_Queue


# redis接收消息
class Minion_Check_Worker(object):
    def __init__(self):

        self.worker = Redis_Queue('check_minion')
        self.radio = self.worker.subscribe()


    def start(self):
        print('Minion Check Worker 已启动')
        while True:
            # 接收队列消息
            msg = self.radio.parse_response()
            # 解析消息内容
            msg = eval(msg[2])
            if msg['add']:
                time.sleep(5)
            # 调用test.ping测试
            minion_check = Test_ping()
            # 检测主机配置
            grains = Grains()
            if msg['pattern'] == 1: # 检测主机
                minion_check.get_status(msg['id'])
            if msg['pattern'] == 2: # 获取主机信息
                grains.get_minion_items(msg['id'])

class Execute_State_Worker(object):
    def __init__(self):
        self.worker = Redis_Queue('execute_state')
        self.radio = self.worker.subscribe()


    def start(self):
        print('Execute State Worker 已启动')
        while True:
            # 接收队列消息
            msg = self.radio.parse_response()
            print(msg)
            # 解析消息内容
            msg = eval(msg[2])
            print('接收：', msg)
            # 执行状态
            state_sls = State_sls()
            if msg['pattern'] == 1: # 执行状态
                response = {'id':None,'code':None,'msg':None}
                result = state_sls.execute_state(minion_id=msg['id'],sls=msg['sls'])
                if result:
                    response['id'] = id
                    response['code'] = 0
                    response['msg'] = result
                else:
                    response['id'] = id
                    response['code'] = 9527
                    response['msg'] = result
                return response

if __name__=='__main__':
    exe_state = Execute_State_Worker()
    exe_state.start()