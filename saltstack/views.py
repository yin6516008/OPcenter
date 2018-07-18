import datetime,time,os,shutil,yaml
import json
import subprocess
from django.shortcuts import render,redirect,HttpResponse
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from saltstack.models import Accepted_minion,Project,PlayBook,Async_jobs
from saltstack.salt_manage import Key_manage,Master_manage,PlayBook_manage,Minion_state
from login.AuthLogin import check_login
from Aladdin.RedisQueue import Redis_Queue
from OPcenter.settings import SUCCESS_DATA
from OPcenter.settings import EXCEPT_DATA
from saltstack.forms import PlayBookForm
# Create your views here.

# 主机列表：minion_list=已添加；unaccepted_list=待添加
@check_login
def salt_minions(request,page=1):
    if request.method == "GET":
        key_manage = Key_manage()
        # 已经允许的salt-key
        accepted_list = key_manage.accepted_minion()
        # 未允许的salt-key
        unaccepted_list = key_manage.unaccepted_minion()
        # 查询出以允许的Key的主机信息
        minion_list = Accepted_minion.objects.all().order_by('-salt_id')
        # 列出分组信息
        project_list = Project.objects.all().order_by('-id')
        # 如果salt-key已经不存在，则标记异常:status=3
        for minion in minion_list.values('id'):
            if minion['id'] not in accepted_list:
                exception_minion = (minion['id'])
                Accepted_minion.objects.filter(id=exception_minion).update(status=3)
        # 每页page_row_num条，生成分页实例paginator对象
        page_row_num = 15
        paginator = Paginator(minion_list, page_row_num)
        # 获取指定页码的数据
        try:
            one_page = paginator.page(page)
        except PageNotAnInteger:
            one_page = paginator.page(1)
        except EmptyPage:
            one_page = paginator.page(paginator.num_pages)
        where = {'id': '', 'ip': '', 'os': '', 'project': ''}
        data = {
            'one_page': one_page,
            'paginator':paginator,
            'start': (int(page)-1)*page_row_num,
            'project_list':project_list,
            'where': where,
            'url': '/saltstack/minion_list/',
            'unaccepted_list': unaccepted_list,
        }
        # 返回页面
        return render(request, 'saltstack_minion_list.html',{'data':data})

# 主机搜索
@check_login
def minion_search(request,page=1):
    if request.method == "GET":
        # 如果搜索条件为空，则赋值一个字符串
        id = 'Empty_value' if request.GET.get('id') == '' else request.GET.get('id')
        ip = 'Empty_value' if request.GET.get('ip') == '' else request.GET.get('ip')
        project = 'Empty_value' if request.GET.get('project') == '' else request.GET.get('project')
        if project is not None:
            where = {'id':id,'ip':ip,'project':project}
            # 多个字段模糊查询， 双下划线前是字段名,icontains 包含 忽略大小写 ilike ‘%aaa%’
            #minion_list = Accepted_minion.objects.filter(Q(id__icontains=where['id']) | Q(ipv4__icontains=where['ip']) | Q(osfinger__icontains=where['os']) | Q(project__id=where['project'])).order_by('-salt_id')
            minion_list = Accepted_minion.objects.filter(project__id=where['project']).order_by('-salt_id')
        else:
            # 如果搜索条件全部为空，则回到主机列表页
            if id == ip == 'Empty_value':
                return redirect('/saltstack/')
            # 如果组名不存在，则 project_id = 0  （0代表不存在的）
            project_item = Project.objects.filter(name=project).values()
            project_id = 0 if project_item.count() == 0 else project_item[0]['id']
            # 构建查询条件字典
            where = {'id':id,'ip':ip,'project':project_id}
            # 多个字段模糊查询， 双下划线前是字段名,icontains 包含 忽略大小写 ilike ‘%aaa%’
            minion_list = Accepted_minion.objects.filter(Q(id__icontains=where['id']) | Q(ipv4__icontains=where['ip']) | Q(project__id=where['project'])).order_by('-salt_id')

        # 每页page_row_num条，生成分页实例paginator对象
        page_row_num = 15
        paginator = Paginator(minion_list, page_row_num)
        # 获取指定页码的数据
        try:
            one_page = paginator.page(page)
        except PageNotAnInteger:
            one_page = paginator.page(1)
        except EmptyPage:
            one_page = paginator.page(paginator.num_pages)
        # 项目组列表
        project_list = Project.objects.all().order_by('-id')
        # 未添加的主机选项卡，未允许的salt-key
        key_manage = Key_manage()
        unaccepted_list = key_manage.unaccepted_minion()

        data = {
            'one_page': one_page,                   # 一页的内容
            'paginator':paginator,                  # 分页实例
            'start': (int(page)-1)*page_row_num,    # 每页序号开始的数字
            'where':where,                          # 搜索条件
            'url': '/saltstack/minion_search/',     # 搜索url
            'unaccepted_list':unaccepted_list,      # 未添加的主机列表
            'project_list':project_list,
        }
        # 返回页面
        return render(request, 'saltstack_minion_list.html',{'data':data})

# 添加主机
@check_login
def minion_add(request):
    if request.method == "POST":
        id = request.POST.get('id')
        ipv4 = request.POST.get('ipv4')
        city = request.POST.get('city')
        now_time = datetime.datetime.fromtimestamp(time.time())
        status = 2 #检测状态：0=离线，1=正常，2=检测中
        # salt-key允许加入
        key_manage = Key_manage()
        key_manage.accept_key(minion_id=id)
        # 主机信息入库
        Accepted_minion.objects.create(id=id,ipv4=ipv4,city=city,datetime=now_time,status=status)
        # 发送检测任务到redis队列
        monion_check = Redis_Queue('check_minion')
        # 模式1=test.ping,2=grains.items
        test = {'pattern': 1,'id': [id],'add':True}
        monion_check.publish(test)
        grains = {'pattern': 2,'id': id,'add':True}
        monion_check.publish(grains)

        SUCCESS_DATA['data'] = '添加成功'
        msg = SUCCESS_DATA
        # 返回结果
        return HttpResponse(json.dumps(msg))

# 检测主机状态
@check_login
def minion_test(request):
    if request.method == "POST":
        # 接收id
        id = request.POST.get('id')
        # 实例化Redis
        monion_check = Redis_Queue('check_minion')
        # 刷新列表，检测全部主机
        if id == '*':
            Accepted_minion.objects.update(status=2)
            minion_id_dict = Accepted_minion.objects.values('id')
            minion_id_list = []
            for minion_id in minion_id_dict:
                minion_id_list.append(minion_id['id'])
            # 发送检测任务到redis队列   # pattern模式1=test.ping,2=grains.items
            test = {'pattern': 1, 'id': minion_id_list,'add':False}
            monion_check.publish(test)
            # 返回结果
            SUCCESS_DATA['data'] = '检测中'
            msg = SUCCESS_DATA
            return HttpResponse(json.dumps(msg))

        # 批量检测部分主机
        else:
            salt_id_list = json.loads(request.POST.get('id'))
            id_list = Accepted_minion.objects.in_bulk(salt_id_list).values()
            # 发送检测任务到redis队列   # pattern模式1=test.ping,2=grains.items
            minion_id_list = []
            # 更新数据库
            for id in id_list:
                minion_id_list.append(str(id))
                Accepted_minion.objects.filter(id=id).update(status=2)
            test = {'pattern': 1, 'id': minion_id_list, 'add': False}
            monion_check.publish(test)
            #返回页面
            SUCCESS_DATA['data'] = '检测中'
            msg = SUCCESS_DATA
            return HttpResponse(json.dumps(msg))

# 删除主机
@check_login
def minion_del(request):
    if request.method == "POST":
        id = request.POST.get('id')
        id = ['md_linux_op_node1_local_vmm',]
        for id in id:
            key_manage = Key_manage()
            key_manage.reject_key(id)
            Accepted_minion.objects.filter(id=id).delete()
        # 返回结果
        SUCCESS_DATA['data'] = '删除成功'
        msg = SUCCESS_DATA
        return HttpResponse(json.dumps(msg))

# 剧本管理
@check_login
def playbook(request):
    if request.method == 'GET':
        playbook_list = PlayBook.objects.all().order_by('-id')
        project_list = Project.objects.all().values().order_by('-id')
        data = {'playbook_list':playbook_list,
                'project_list':project_list,
                }
        return render(request, 'saltstack_playbook.html',{'data':data})

# 剧本分组筛选
@check_login
def playbook_project(request,project):
    if request.method == "GET":
        playbook_list = PlayBook.objects.filter(project__name=project).order_by('id')
        project_list = Project.objects.all().values().order_by('-id')
        data = {'playbook_list': playbook_list,
                'project_list': project_list,
                }
        return render(request, 'saltstack_playbook.html', {'data': data})

# 剧本上传
@check_login
def playbook_upload(request):
    if request.method == 'POST':
        file_obj = request.FILES
        playbook_m_obj = PlayBook_manage()
        result = playbook_m_obj.file_upload(file_obj)
        return HttpResponse(json.dumps(result))

# 剧本编辑
@check_login
def playbook_edit(request):
    if request.method == 'POST':
        playbook_id = request.POST.get('playbook_id')
        plabook_obj = PlayBook.objects.get(id=playbook_id)

        if os.path.exists(plabook_obj.applied_file):
            with open(plabook_obj.applied_file, 'r') as f:
                file_context = f.read()
            SUCCESS_DATA['data'] = {
                'playbook_content':file_context,
                'playbook_path':plabook_obj.applied_file
            }
            return HttpResponse(json.dumps(SUCCESS_DATA))
        else:
            EXCEPT_DATA['data'] = {
                'playbook_content':'文件不存在',
                'playbook_path':plabook_obj.applied_file
            }
            return HttpResponse(json.dumps(EXCEPT_DATA))

# 剧本保存
@check_login
def playbook_save(request):
    if request.method == 'POST':
        playbook_path = request.POST.get('playbook_path')
        playbook_context = request.POST.get('playbook_context')
        print('*'*10,playbook_path,'\n',playbook_context)
        playbook_m_obj = PlayBook_manage()
        result = playbook_m_obj.save(playbook_path,playbook_context)
        if result:
            with open(playbook_path, 'r') as f:
                playbook_content = f.read()
            SUCCESS_DATA['data'] = {'msg':'保存修改成功',
                                    'playbook_content':playbook_content,
                                    'playbook_path': playbook_path,
                                    }
            return HttpResponse(json.dumps(SUCCESS_DATA))
        else:
            EXCEPT_DATA['data'] = {'msg':'保存修改失败',
                                    'playbook_content':result,
                                    'playbook_path': playbook_path,
                                    }
            return HttpResponse(json.dumps(EXCEPT_DATA))

# 剧本删除
@check_login
def playbook_del(request):
    if request.method == 'POST':
        playbook_path = request.POST.get('playbook_path')
        playbook_m_obj= PlayBook_manage()
        result = playbook_m_obj.delete(playbook_path)
        if result:
            SUCCESS_DATA['data'] = playbook_path+'删除成功'
            return HttpResponse(json.dumps(SUCCESS_DATA))
        else:
            EXCEPT_DATA['data'] = playbook_path+result
            return HttpResponse(json.dumps(EXCEPT_DATA))

# 执行剧本主页
@check_login
def playbook_exe(request):
    if request.method == "GET":

        project_list = Project.objects.all().order_by('-id')
        minion_list = Accepted_minion.objects.all().order_by('-id')
        playbook_list = PlayBook.objects.exclude(sls__icontains='文件').order_by('-id')
        jobs_list = Async_jobs.objects.defer('information').order_by('-id')
        data = {'project_list':project_list,
                'minion_list':minion_list,
                'playbook_list':playbook_list,
                'jobs_list':jobs_list,
                }
        return render(request, 'saltstack_playbook_exe.html', {'data': data})

# 按分组筛选
@check_login
def playbook_exe_project(request,project):
    if request.method == "GET":
        project_list = Project.objects.all().values().order_by('-id')
        minion_list = Accepted_minion.objects.filter(project__name=project).order_by('-id')
        playbook_list = PlayBook.objects.filter(project__name=project).exclude(sls__icontains='文件').order_by('-id')
        jobs_list = Async_jobs.objects.defer('information').filter(project__name=project).order_by('-id')

        data = {'project_list':project_list,
                'minion_list':minion_list,
                'playbook_list':playbook_list,
                'jobs_list':jobs_list,
                }
        return render(request, 'saltstack_playbook_exe.html', {'data': data})

# 执行剧本操作
@check_login
def playbook_exe_sls(request):
    if request.method == "POST":
        minion_id_list = json.loads(request.POST.get('minion_id_list'))
        playbook_id = request.POST.get('playbook_id')

        # 生成任务编号number=yyyymmdd+000
        last = Async_jobs.objects.last()
        today = datetime.date.today().strftime('%Y%m%d')
        try:
            number = str(int(last.number)+1) if last.number[0:8] == today else today+'001'
        except AttributeError:
            number = today+'001'

        # 发布消息
        state_execute = Redis_Queue('state_execute')
        state_param = {'number': number, 'minion_id_list': minion_id_list, 'playbook_id': playbook_id}
        state_execute.publish(state_param)

        # 写入数据库
        create_time = datetime.datetime.fromtimestamp(time.time())

        description = PlayBook.objects.get(id=playbook_id)

        jobs_info = Async_jobs(number=number, description=description, project=description.project, create_time=create_time, status=0)
        jobs_info.save()
        try:
            jobs_info.minion.add(*minion_id_list)
        except Exception as error:
            # 异常返回
            EXCEPT_DATA['data'] = {'number':number,
                                   'description': str(description),
                                   'create_time': create_time.strftime("%H:%M:%S"),
                                   'error':error,
                                   }
            return HttpResponse(json.dumps(EXCEPT_DATA))
        # 成功返回
        SUCCESS_DATA['data'] = {'number':number,
                                'description':str(description),
                                'create_time':create_time.strftime("%H:%M:%S"),
                                'success':'Join the queue',
                                }

        return HttpResponse(json.dumps(SUCCESS_DATA))

def playbook_exe_result(request):
    if request.method == "POST":
        number = request.POST.get('number')
        job_obj = Async_jobs.objects.get(number=number)
        information = str(job_obj.information)
        return  HttpResponse(information)
# 远程终端

