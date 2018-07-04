import time,datetime
import os,shutil
import subprocess
import redis
from salt import client,config,loader,key
from saltstack.models import Accepted_minion
# from saltstack.models import Unaccepted_minion
# from saltstack.models import Exception_minion
from Aladdin import PathTreeList

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
            print(err)
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
    def get_minion_items(self,minion_id):
        # 定义需要获取的信息
        items = ['id', 'osfinger', 'cpu_model', 'cpuarch', 'num_cpus', 'mem_total']
        minion_items = []
        # 获取minion_id的硬件信息
        result = self.cmd(minion_id, 'grains.item', items)
        for id in result.keys():
            items = result[id]
            print(items)
            now_time = datetime.datetime.fromtimestamp(time.time())
            if items:
                items['datetime'] = now_time
                mem_gib = 0.5 if round((items['mem_total'])/1024) == 0 else round((items['mem_total'])/1024)
                items['mem_gib'] = mem_gib
                Accepted_minion.objects.filter(id=id).update(**items)
            else:
                Accepted_minion.objects.filter(id=id).update(status=0,datetime=now_time)
        return  result

# test模块
class Test_ping(client.LocalClient):
    # 获取主机的状态
    def get_status(self,minion_id):
        # id不能为空，避免异常
        if minion_id is not None:
            # 接收test.ping的返回结果
            print(minion_id)
            result = self.cmd(minion_id,'test.ping',[])
            #result必然是一个字典
            print(result)
            for id in result.keys():
                status = 1 if result[id] else 0 # True=1；False=0
                # 检测状态更新到数据库
                Accepted_minion.objects.filter(id=id).update(status=status)
            return result

# cmd模块远程执行------------------
class Cmd_run(client.LocalClient):
    # win系统
    def cmd_for_win(self,minion_id,cmd):
        result = self.cmd(minion_id, 'cmd.powershell', [cmd])
        print(result)
        return result

    # linux系统
    def cmd_for_linux(self,minion_id,cmd):
        result = self.cmd(minion_id, 'cmd.run', [cmd])
        print(result)
        return result

# file模块的使用-------------------
class File_manage(client.LocalClient):
    # 文件权限检测
    def access(self,minion_id,dst_file):
        result = self.cmd(minion_id, 'file.access', [dst_file, 'f'])
        print('file.access', result)
        return result

    # 检测文件是否存在
    def exists(self,minion_id,dst_file):
        result = self.cmd(minion_id, 'file.exists', [dst_file])
        print('file.exists', result)
        return result

    # 检测路径是否有效
    def directory_exists(self,minion_id,dst_path):
        result = self.cmd(minion_id, 'file.directory_exists', [dst_path])
        print('file.directory_exists', result)
        return result

    # 从绝对路径中截取文件名
    def basename(self,minion_id,dst_file):
        result = self.cmd(minion_id,'file.basename',[dst_file])
        print('file.basename', result)
        return result

    # 从绝对路径中截取目录
    def dirname(self,minion_id,dst_file):
        result = self.cmd(minion_id,'file.dirname',[dst_file])
        print('file.dirname', result)
        return result

    # 文件覆盖写入
    def write(self,minion_id,dst_file,context):
        result = self.cmd(minion_id, 'file.write', [dst_file, context])
        print('file.write', result)
        return result

    # 文件追加写入
    def append(self,minion_id,dst_file,context):
        result = self.cmd(minion_id, 'file.append', [dst_file, context])
        print('file.append', result)
        return result

    # 读取文件的内容
    def read(self,minion_id,dst_file):
        result = self.cmd(minion_id,'file.read',[dst_file,'binary = False'])
        print('file.read', result)
        return result

    # 返回文件夹包含的文件列表
    def readdir(self,minion_id,dst_path):
        result = self.cmd(minion_id,'file.readdir',[dst_path])
        print('file.readdir', result)
        return result

    # 重命名文件或文件夹
    def rename(self,minion_id,src_path,dst_path):
        result = self.cmd(minion_id, 'file.rename', [src_path, dst_path])
        print('file.rename', result)
        return result

    # 文件本地拷贝，源文件在minion本地
    def copy_local(self,minion_id,src_file,dst_file):
        result = self.cmd(minion_id, 'file.copy', [src_file, dst_file])
        print('local_copy', result)
        return result

class Copy_remote(client.LocalClient):
    # 远程拷贝目录，源文件在master
    def get_file(self,minion_id,src_file,dst_file):
        result = self.cmd(minion_id, 'cp.get_file', [src_file, dst_file])
        print('remote_copy', result)
        return result

    # 远程拷贝文件，源文件在master
    def get_dir(self,minion_id,src_path,dst_path):
        result = self.cmd(minion_id, 'cp.get_dir', [src_path, dst_path])
        print('remote_copy', result)
        return result

    # 远程拷贝文件，源文件在salt://, http://, https://, ftp://, s3://, swift://
    def get_url(self,minion_id,src_url,dst_path):
        result = self.cmd(minion_id, 'cp.get_url', [src_url, dst_path])
        print('remote_copy', result)
        return result

class Configuration(object):
    def __init__(self):
        self.client =  client.LocalClient
        # salt安装目录
        self.salt_dir = '/etc/salt/'
        # salt文件管理目录
        self.file_roots = '/srv/salt/base'
        # 配置文件导入目录 sls_conf
        self.sls_conf = '%s/saltstack/sls_conf/' % os.getcwd()

    # 可导入的配置
    def import_files(self):
        if os.path.exists(self.sls_conf):
            sls_conf = PathTreeList.path_list(self.sls_conf)
            return sls_conf
        else:
            return False

    # 已导入可执行的配置
    def imported_files(self):
        if os.path.exists(self.file_roots):
            file_roots = PathTreeList.path_list(self.file_roots)
            return file_roots
        else:
            return False

    # 查看和编辑
    def file_edit(self,edit_file):
        with open(self.sls_conf + edit_file, 'r') as f:
            return f.read()

    # 执行初始化
    def master_init(self):
        # 判断salt安装与否
        if os.path.exists(self.salt_dir):
            # 创建salt文件目录
            if not os.path.exists('/srv/salt'): # 基础环境目录
                os.makedirs('/srv/salt')
            if not os.path.exists('/srv/salt/init'): # 初始化配置目录
                os.makedirs('/srv/salt/init')
            if not os.path.exists('/srv/salt/test'): # 测试环境目录
                os.makedirs('/srv/salt/test')
            if not os.path.exists('/srv/salt/prod'): # 生产环境目录
                os.makedirs('/srv/salt/prod')

            # 备份master配置文件
            if os.path.exists(self.salt_dir+'master'):
                master_bak = 'master_' + datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')
                os.rename(self.salt_dir+'master', self.salt_dir+master_bak)
                # 删除90天前的master_前缀的配置文件备份
                for master_bak in os.listdir(self.salt_dir):
                    if master_bak.startswith('master_') and time.time() - os.path.getmtime(self.salt_dir+master_bak) > 90*24*3600:
                        os.remove(master_bak)

            # 导入master的配置文件
            shutil.copyfile(self.sls_conf + 'master', self.salt_dir + 'master')
            # 导入基础状态文件
            shutil.copyfile(self.sls_conf + 'env_init.sls', self.file_roots + 'init/')
            # 导入Python状态文件
            shutil.copyfile(self.sls_conf + 'python3.sls', self.file_roots + 'init/')

            # 检查配置文件
            return True

        else:
            return False

    # 执行初始化
    def execute_init(self,minion_id,sls):
        result = self.client.cmd(minion_id, 'state.sls', [sls])

class File_upload(object):
    pass

class Salt_script(object):
    def __init__(self):
        self.release_code = Copy_remote()

    def release_code(self,id_list):
        # 将需要发布的文件目录挂载到salt目录下
        subprocess.getstatusoutput(
            "mkdir -p /srv/salt/test/OPcenter-slave && mount --bind /opt/OPcenter-slave /srv/salt/test/OPcenter-slave")
        src_path = 'salt://test/OPcenter-slave'
        # 发布到minion的指定目录
        dst_path = '/test1/OPcenter-slave'
        for id in id_list:
            self.release_code.get_dir(id, src_path, dst_path)
        return 'OK'

"""
# test

km = Key_manage()
km.accept_key('md_win_op_node5_local_vmm')

grains = Grains()
grains.get_node_info('md_linux_op_node1_local_vmm')
grains.get_node_info('md_win_op_node5_local_vmm')

lc = Cmd_run()
lc.cmd_for_win('md_win_op_node5_local_vmm','gci . -r | measure -property length -sum')
lc.cmd_for_linux('md_linux_op_node1_local_vmm','df -h')

fm = File_manage()
fm.access('md_linux_op_node1_local_vmm','/tmp/abc.py')
fm.write('md_linux_op_node1_local_vmm','/tmp/abc.py','写入到src')
fm.append('md_linux_op_node1_local_vmm','/tmp/abc.py','追加到src')
fm.basename('md_linux_op_node1_local_vmm','/tmp/abc.py')
fm.local_copy('md_linux_op_node1_local_vmm','/tmp/1salt.py','/tmp/abc.py')
fm = File_manage()
fm.remote_copy('*','salt://base/prod/OPcenter-slave','/opt/OPcenter-slave')
"""
