import datetime,time
import json
import subprocess
from django.shortcuts import render,redirect,HttpResponse
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from saltstack.models import Accepted_minion
from saltstack.salt_manage import Key_manage,Cmd_run,Configuration,State_sls
from login.AuthLogin import check_login
from Aladdin.RedisQueue import Redis_Queue
from OPcenter.settings import SUCCESS_DATA
from OPcenter.settings import EXCEPT_DATA
# Create your views here.

# 主机列表：minion_list=已添加；unaccepted_list=待添加
def accepted_list(request,page=1):
    if request.method == "GET":
        key_manage = Key_manage()
        # 已经允许的salt-key
        accepted_list = key_manage.accepted_minion()
        # 未允许的salt-key
        unaccepted_list = key_manage.unaccepted_minion()
        # 查询出以允许的Key的主机信息
        minion_list = Accepted_minion.objects.all().order_by('-salt_id')
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

        data = {
            'url': '/saltstack/minion_list/',
            'one_page': one_page,
            'paginator':paginator,
            'start': (int(page)-1)*page_row_num,
        }
        # 返回页面
        return render(request, 'host_list.html',{'data':data,'unaccepted_list':unaccepted_list})

def minion_search(request,page=1):
    if request.method == "GET":
        # 如果搜索条件为空，则赋值一个字符串
        id = 'Empty_value' if request.GET.get('id') == '' else request.GET.get('id')
        ip = 'Empty_value' if request.GET.get('ip') == '' else request.GET.get('ip')
        os = 'Empty_value' if request.GET.get('os') == '' else request.GET.get('os')
        if id == ip == os == 'Empty_value':
            return redirect('/saltstack/')
        where = {'id':id,'ip':ip,'os':os}
        # 多个字段模糊查询， 双下划线前是字段名,icontains 包含 忽略大小写 ilike ‘%aaa%’
        minion_list = Accepted_minion.objects.filter(Q(id__icontains=where['id']) | Q(ipv4__icontains=where['ip']) | Q(osfinger__icontains=where['os'])).order_by('-salt_id')
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

        data = {
            'url':'/saltstack/minion_search/',
            'one_page': one_page,
            'paginator':paginator,
            'start': (int(page)-1)*page_row_num,
            'where':where,
        }
        # 未添加的主机选项卡，未允许的salt-key
        key_manage = Key_manage()
        unaccepted_list = key_manage.unaccepted_minion()
        # 返回页面
        return render(request, 'host_list.html',{'data':data,'unaccepted_list':unaccepted_list})

# 添加主机
def minion_add(request):
    if request.method == "POST":
        id = request.POST.get('id')
        ipv4 = request.POST.get('ipv4')
        city = request.POST.get('city')
        now_time = datetime.datetime.fromtimestamp(time.time())
        status = 2 #检测状态：0=异常，1=正常，2=检测中
        # salt-key允许加入
        key_manage = Key_manage()
        key_manage.accept_key(minion_id=id)
        # 主机信息入库
        Accepted_minion.objects.create(id=id,ipv4=ipv4,city=city,datetime=now_time,status=status)
        # 发送检测任务到redis队列
        time.sleep(3)
        monion_check = Redis_Queue('check_minion')
        # 模式1=test.ping,2=grains.items
        test = {'pattern': 1,'id': id}
        monion_check.publish(test)
        grains = {'pattern': 2,'id': id}
        monion_check.publish(grains)

        SUCCESS_DATA['data'] = '添加成功'
        msg = SUCCESS_DATA
        print(msg)
        # 返回结果
        return HttpResponse(json.dumps(msg))

# 检测/刷新主机状态
def minion_test(request):
    if request.method == "POST":
        monion_check = Redis_Queue('check_minion')
        # 批量检测部分主机状态
        try:
            for id in json.loads(request.POST.get('id')):
                # 发送检测任务到redis队列   # pattern模式1=test.ping,2=grains.items
                test = {'pattern':1,'id': id}
                monion_check.publish(test)
                # 更新数据库
                Accepted_minion.objects.filter(id=id).update(status=2)
            #返回页面
            SUCCESS_DATA['data'] = '检测中'
            msg = SUCCESS_DATA
            return HttpResponse(json.dumps(msg))
            #return redirect('/saltstack/')
        # 检测一个id或*全部
        except Exception as e:
            id = request.POST.get('id')
            # 发送检测任务到redis队列   # pattern模式1=test.ping,2=grains.items
            test = {'pattern': 1, 'id': id}
            monion_check.publish(test)
            grains = {'pattern': 2, 'id': id}
            monion_check.publish(grains)
            # 更新数据库
            if id == '*':
                Accepted_minion.objects.all().update(status=2)
            else:
                Accepted_minion.objects.filter(id=id).update(status=2)
            # 返回结果
            SUCCESS_DATA['data'] = '检测中'
            msg = SUCCESS_DATA
            return HttpResponse(json.dumps(msg))

@check_login
def minion_del(request):
    if request.method == "POST":
        id = request.POST.get('id')
        print(id)
        id = ['md_linux_op_node1_local_vmm',]
        for id in id:
            key_manage = Key_manage()
            key_manage.reject_key(id)
            Accepted_minion.objects.filter(id=id).delete()
        # 返回结果
        SUCCESS_DATA['data'] = '删除成功'
        msg = SUCCESS_DATA
        return HttpResponse(json.dumps(msg))

def minion_control(request):
    if request.method == "POST":
        cmdstr = request.POST.get('cmd')
        cmd_run = Cmd_run()
        cmdstr = 'df -h'
        result = cmd_run.cmd_for_linux('*',cmdstr)
        return HttpResponse(json.dumps(result))


def file_editor(request):
    if request.method == "POST":
        conf = Configuration()
        filename = request.POST.get('edit_file')
        master_info = conf.file_edit(filename)
        print(master_info)
        #return HttpResponse(master_info)
        return render(request, 'show_editor.html', {'master_info':master_info})


def control_center(request):
    if request.method == "GET":
        conf = Configuration()
        # 主机列表
        host_list = Accepted_minion.objects.all().order_by('-id')
        # 已导入的脚本列表
        imported_files = conf.imported_files()

        data = {
            'host_list': host_list,
            'script':imported_files
        }
        return render(request, 'host_operate.html', {'data': data})

    if request.method == "POST":
        id = request.POST.get('id')
        sls = request.POST.get('sls')
        monion_check = Redis_Queue('execute_state')
        task_id = time.time()
        for id in id:
            msg = {'pattern': 1, 'id': id,'sls':sls,'task_id':task_id}
            monion_check.publish(msg)
        return HttpResponse({'msg':task_id})
