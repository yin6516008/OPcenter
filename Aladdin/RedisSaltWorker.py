from redis import Redis
import django
import os,sys,time,datetime,json
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.chdir(BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "OPcenter.settings")
django.setup()
from django.conf import settings
from saltstack.salt_manage import Test_ping,Grains,Minion_state,Key_manage
from saltstack.models import Accepted_minion,Async_jobs
from django.db.models import Q
from salt import client

redis_id = settings.REDIS_IP
redis_password = settings.REDIS_PASSWORD
from Aladdin.RedisQueue import Redis_Queue


# redis接收检测命令
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

# 自动任务
class Saltstack_Auto_Worker(object):
    def __init__(self):
        # 设定自动执行的间隔时间
        self.interval = 200
        # 实例化检测队列
        self.check_minion = Redis_Queue('check_minion')

    def start(self):
        print('Saltstack Auto Worker 已启动')
        while True:

            # -----------------定时统计主机执行剧本的次数---开始-------------------------
            minion_id_list = Accepted_minion.objects.all()
            for minion_obj in minion_id_list:
                jobs_count = Async_jobs.objects.filter(minion__id=minion_obj.id).count()
                Accepted_minion.objects.filter(id=minion_obj.id).update(jobs_count=jobs_count)
            # -----------------定时统计主机执行剧本的次数---结束-------------------------

            time.sleep(self.interval)

            # -----------------自动检测执行剧本排队异常---开始---------------------------
            # 0=排队 1=执行中 2=执行完成 3=异常
            hours_ago = datetime.datetime.fromtimestamp(time.time()-3600*3)
            except_jobs = Async_jobs.objects.defer('information').filter(Q(status=0) | Q(status=1) & Q(create_time__lte=hours_ago))
            for job in except_jobs:
                if job.status == 0 :
                    Async_jobs.objects.filter(id=job.id).update(status=3,success_total=0)
                elif job.status == 1 and job.information is not None:
                    try:
                        Async_jobs.objects.filter(id=job.id).update(status=2,success_total=eval(job.information)['success'])
                    except Exception:
                        Async_jobs.objects.filter(id=job.id).update(status=2, success_total=0)
                else:
                    Async_jobs.objects.filter(id=job.id).update(status=3,success_total=0)
            # -----------------自动检测执行剧本排队异常---结束---------------------------

            time.sleep(self.interval)

            # -----------------自动检测在线离线---开始----------------------------------
            minion_id_list = []
            # 从salt-key获取所有minion
            key_manage = Key_manage()
            accepted_list = key_manage.accepted_minion()
            # 从数据库获取所有minion
            minion_id_dict = Accepted_minion.objects.values('id')
            # 判断数据库中的minion有效性，添加到minion_id_list
            for minion_item in minion_id_dict:
                if minion_item['id'] in accepted_list:
                    minion_id_list.append(minion_item['id'])
                else:
                    # salt-key已不存在，标记为异常:status=3
                    now_time = datetime.datetime.fromtimestamp(time.time())
                    errinfo = {'datetime': now_time, 'status': 3, 'cpu_model': '', 'osfinger': '不存在的salt-key','mem_gib': 0, 'mem_total': 0, 'num_cpus': 0, }
                    Accepted_minion.objects.filter(id=minion_item['id']).update(**errinfo)
            # 发送检测消息到队列
            test = {'pattern': 1,'id':minion_id_list,'add':False}
            self.check_minion.publish(test)
            # -----------------自动检测在线离线---结束----------------------------------

            # 等待进入下一回合
            time.sleep(self.interval)


# 接收剧本执行命令
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
            jid = result[0]
            number = result[1]
            t = 1
            # 判断异常
            if result[0] not in msg['minion_id_list'] and type(jid) == int and jid > 0:
                # 持续查询，直到出现结果，或者连接超时
                while not self.client.get_cache_returns(jid):
                    time.sleep(1)
                    if t == 1200:
                        information = {'ERROR':'Timeout'}
                        break
                    else:
                        t += 1
                else:
                    information = self.client.get_cache_returns(jid)
                # 继续查询，直到全部主机执行结果全部得到
                if len(information) != len(msg['minion_id_list']) and 'ERROR' not in information:
                    while len(self.client.get_cache_returns(jid)) != len(msg['minion_id_list']):
                        time.sleep(1)
                        if t == 1200:
                            information = self.client.get_cache_returns(jid)
                            minion_id_obj = Accepted_minion.objects.in_bulk(msg['minion_id_list']).values()
                            for minion_id in minion_id_obj:
                                if str(minion_id) not in information:
                                    information[str(minion_id)] = {'ret': ['Timeout']}
                            break
                        else:
                            t += 1
                    else:
                        information = self.client.get_cache_returns(jid)
                minion_state.save_sls(number=number,information=information)
                print('任务完成，state_execute频道继续接收消息')
            else:
                information = {'ERROR':'未选择主机或剧本'} if jid == 0 else {'不存在的主机':result[0]}
                minion_state.save_sls(number=number, information=information)
                print('任务异常，state_execute频道继续接收消息')
                continue
                # 继续订阅

