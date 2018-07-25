import time,datetime,os,shutil,json
from salt import client,config,loader,key
from saltstack.models import Accepted_minion,PlayBook,Project,Async_jobs
from saltstack.salt_sls_ret_format import PlayBookResponse
from OPcenter.settings import BASE_DIR,SUCCESS_DATA,EXCEPT_DATA

# 管理key
class Key_manage(object):
    def __init__(self):
        self.opts = config.master_config('/etc/salt/master')
        self.keys = key.get_key(self.opts)

    # key列出----------------------------------
    # 列出全部minion的key
    def all_keys(self):
        all_keys = self.keys.list_keys()
        return all_keys

    # 已添加的minion
    def accepted_minion(self):
        accepted =  self.all_keys()['minions']
        return accepted

    # 待添加的minion
    def unaccepted_minion(self):
        unaccepted = self.all_keys()['minions_pre']
        return unaccepted

    # 已经拒绝的minion
    def rejected_minion(self):
        rejected = self.all_keys()['minions_rejected']
        return rejected

    # key操作---------------------------------
    # 添加minion
    def accept_key(self,minion_id):
        try:
            self.keys.accept(minion_id)
            return True
        except Exception as err:
            return err

    # 拒绝minion的key
    def reject_key(self,minion_id):
        try:
            self.keys.reject(minion_id)
            return True
        except Exception as err:
            return err

    # 删除minion的key
    def delete_key(self,minion_id):
        try:
            self.keys.delete_key(minion_id)
            return True
        except Exception as err:
            return err

# Grains的使用----------------
class Grains(client.LocalClient):
    # grains获取节点信息
    def get_minion_items(self,minion_id_list):
        # 定义需要获取的信息
        items = ['id', 'osfinger', 'cpu_model', 'num_cpus', 'mem_total']
        # 获取minion_id的硬件信息
        result = self.cmd(minion_id_list, 'grains.item', items,tgt_type='list')
        for id in result.keys():
            items = result[id]
            now_time = datetime.datetime.fromtimestamp(time.time())
            if type(items) == dict:
                items['datetime'] = now_time
                mem_gib = 0.5 if round((items['mem_total'])/1024) == 0 else round((items['mem_total'])/1024)
                items['mem_gib'] = mem_gib
                items['status'] = 1
                Accepted_minion.objects.filter(id=id).update(**items)
            else:
                errinfo={'id':id,'datetime': now_time, 'status': 0, 'cpu_model': '主机不在线', 'osfinger': '主机不在线', 'mem_gib': 0, 'mem_total': 0,'num_cpus': 0,}
                Accepted_minion.objects.filter(id=id).update(**errinfo)
        return  result

# test模块
class Test_ping(client.LocalClient):
    # 获取主机的状态
    def get_status(self,minion_id_list):
        # id不能为空，避免异常
        if minion_id_list is not None:
            # 接收test.ping的返回结果
            result = self.cmd(minion_id_list,'test.ping',[],tgt_type='list')
            #result必然是一个字典
            # 更新数据库
            for id in result.keys():
                now_time = datetime.datetime.fromtimestamp(time.time())
                status = 1 if result[id] else 0 # True=1；False=0
                # 检测状态更新到数据库
                Accepted_minion.objects.filter(id=id).update(status=status,datetime=now_time)
            return result

# master配置
class Master_manage():
    def __init__(self):
        # 配置文件导入目录 sls_conf
        self.init_conf = '%s/saltstack/init_conf/' % BASE_DIR
        self.state_sls = '%s/saltstack/state_sls/' % BASE_DIR
        self.salt_etc = '/etc/salt/'
        self.srv_salt = '/srv/salt/'
    # master配置初始化
    def master_init(self):
        # 判断salt安装与否
        if os.path.exists(self.salt_etc):

            # Grains自定义目录
            grains_path = self.srv_salt+'_grains/'
            os.makedirs(grains_path) if not os.path.exists(grains_path) else 'grains path existed'
            # 初始化目录
            init = self.srv_salt+'init'
            os.makedirs(init) if not os.path.exists(init) else 'init path existed'
            # 备份master配置文件
            if os.path.exists(self.salt_etc+'master'):
                master_bak = 'master_' + datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')
                os.rename(self.salt_etc+'master', self.salt_etc+'master_bak')
            # 删除90天前的master_前缀的配置文件备份
            for master_bak in os.listdir(self.salt_etc):
                if master_bak.startswith('master_') and time.time() - os.path.getmtime(self.salt_etc+'master_bak') > 90*24*3600:
                    os.remove(master_bak)
            # 导入master的配置文件
            shutil.copyfile(self.init_conf + 'master', self.salt_etc+'master')
            return True
        else:
            return False

    def grains_defined(self):
        # 导入自定义grains文件
        grains_path = '/srv/salt/_grains/'
        grains_file = '/srv/salt/_grains/grains_defined.py'
        if os.path.exists(grains_file):
            grains_bak = datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f') + '_grains'
            os.rename(grains_file, grains_path + grains_bak)
        shutil.copyfile(self.init_conf + 'grains_defined.py', '/srv/salt/_grains/grains_defined.py')

        result = client.LocalClient().cmd_async('*', 'saltutil.sync_all', [])
        #result = client.LocalClient().cmd(minion_id, 'grains.item', ['md_op_linux_beijing_opcenter-slave','md_op_linux_shanghai_opcenter-slave','md_op_linux_qingdao_opcenter-slave','md_op_linux_shenzhen_opcenter-slave'])
        return result

class PlayBook_manage():
    def __init__(self):
        # 配置文件导入目录 sls_conf
        self.init_conf = '%s/saltstack/init_conf/' % BASE_DIR
        self.state_sls = '%s/saltstack/state_sls/' % BASE_DIR
        self.salt_etc = '/etc/salt/'
        self.srv_salt = '/srv/salt/'

    # 可执行的剧本
    def sls_list(self):
        sls_all = PlayBook.objects.all().values()
        for sls_items in sls_all:
            if not os.path.exists(sls_items['applied_file']):
                PlayBook.objects.filter(id=sls_items['id']).update(status=0)
        sls_list = PlayBook.objects.filter(status=1).values()
        return sls_list


    def file_upload(self,file_obj):
        file_info = file_obj['file_context'].chunks().__next__()
        try:
            project = file_info.decode().splitlines()[0][2:]
            description = file_info.decode().splitlines()[1][2:]
        except Exception as error:
            EXCEPT_DATA['data'] = '必须是utf-8编码：{} '.format(file_obj['file_context'].name)+ str(error)[0:70]
            return EXCEPT_DATA
        project_obj = Project.objects.filter(name=project).first()
        if project_obj is None :
            EXCEPT_DATA['data'] = '不存在的分组：{} '.format(str(project)[0:52])
            return EXCEPT_DATA
        applied_file = os.path.join(self.srv_salt,project_obj.name,file_obj['file_context'].name)
        os.makedirs(os.path.dirname(applied_file)) if not os.path.exists(os.path.dirname(applied_file)) else None
        applied_file_count = PlayBook.objects.filter(applied_file=applied_file).count()
        if applied_file_count != 0 :
            # 返回结果
            EXCEPT_DATA['data'] = '文件名已存在：{} '.format(file_obj['file_context'].name)
            return EXCEPT_DATA
        else:
            # 保存为文件
            with open(applied_file, 'wb') as f:
                for chunk in file_obj['file_context'].chunks():
                    f.write(chunk)
            # 保存到数据库
            # 剧本名
            sls = applied_file[9:-4] if applied_file[-4:] == '.sls' else '%s文件' % applied_file.split('.')[-1]
            PlayBook.objects.create(project_id=project_obj.id,description=description,applied_file=applied_file,sls=sls)
            SUCCESS_DATA['data'] = '上传成功'
            return SUCCESS_DATA

    # 查看和编辑
    def save(self, playbook_path,playbook_context):
        try:
            with open(playbook_path, 'w') as f:
                f.write(playbook_context)
            return True
        except Exception as error:
            return error

    def delete(self,playbook_path):
        try:
            # 删除文件（移动到回收目录）
            playbook_file = os.path.basename(playbook_path)
            recycling = '/srv/salt/Recycling/'
            os.makedirs(recycling) if not os.path.exists(recycling) else None
            shutil.move(playbook_path,recycling+playbook_file)
            # 删除数据库记录
            PlayBook.objects.filter(applied_file=playbook_path).delete()
            return True
        except Exception as error:
            return error

# 执行剧本
class Minion_state(object):
    def __init__(self):
        self.client = client.LocalClient()
    # 执行剧本
    def exe_sls(self,number,minion_id_list, playbook_id):
        # 异步执行状态，minion_list是一个列表，playbook是一个字符串
        try:
            playbook = PlayBook.objects.get(id=playbook_id)
        except Exception as error:
            return (error, number)
        minion_dict_values= Accepted_minion.objects.in_bulk(minion_id_list).values()
        minion_list = []
        for minion_id in minion_dict_values:
            minion_list.append(str(minion_id))
        if len(minion_id_list) == len(minion_list):
            # 异步执行状态，minion_list是一个id列表，playbook.sls是一个剧本字符串
            jid = self.client.cmd_async(minion_list, 'state.sls', [playbook.sls],tgt_type='list')
            # 更新jid到数据库
            start_time = datetime.datetime.fromtimestamp(time.time())
            Async_jobs.objects.filter(number=number).update(jid=jid, start_time=start_time, status=1)
            return (int(jid),number)
        else:
            for salt_id in minion_id_list:
                if Accepted_minion.objects.filter(salt_id=salt_id).values():
                    continue
                else:
                    return (int(salt_id),number)
            else:
                return (0, number)
    # 保存执行结果
    def save_sls(self,number,information):
        finish_time = datetime.datetime.fromtimestamp(time.time())
        if 'ERROR' in information:
            Async_jobs.objects.filter(number=number).update(finish_time=finish_time, status=3,success_total=0,information=json.dumps(information))
        else:
            format_info = PlayBookResponse(information)
            try:
                Async_jobs.objects.filter(number=number).update(finish_time=finish_time, status=2, success_total=format_info.all['success'],information=format_info.all)
            except Exception:
                Async_jobs.objects.filter(number=number).update(finish_time=finish_time, status=2, success_total=0, information=format_info.all)
