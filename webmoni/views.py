from django.shortcuts import render,redirect,HttpResponse
from webmoni.models import DomainName
from webmoni.models import Project
from webmoni.models import Node
from webmoni.models import Event_Log
from webmoni.froms import NodeForms
from django.forms.models import model_to_dict
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from login.AuthLogin import check_login
import datetime,time
import json

# 导入通用的函数
from webmoni.publicFunc import get_areas_data,Domain_table
from Aladdin.RedisQueue import Redis_Queue
from Aladdin.config import Webmoni_Check_Cert_Queue

from django.conf import settings
success_data = settings.SUCCESS_DATA
except_data = settings.EXCEPT_DATA
redis_conn = settings.REDIS


# Create your views here

# 域名状态页面
@check_login
def areas(request,url_id=None):
    """
    :param request:
    :param url_id: 域名在DomainName表里的id
    :return:
        选择域名按钮的内容 = project_list
        数据展示曲线图里的数据 = graph_data
        最下面表格的数据 =  defaultDomainData
    """
    if request.method == 'GET':
        project_list = Project.objects.all().order_by('id')
        defaultDomainData, graph_data = get_areas_data(url_id)
        if graph_data is None and defaultDomainData is None:
            return render(request,"error_page.html",{'errorInfo':'还没有域名,请跳转至域名管理页面添加域名'})
        return render(request,'webmoni_areas.html',{'project_list':project_list,
                                                 'defaultDomainData':defaultDomainData,
                                                 'graph_data':graph_data})

# 创建域名
@check_login
def create(request):
    """
    新建域名函数
    :param request:
    :return:
    """
    if request.method == 'POST':
        check_id = request.POST.get('check_id')
        warning = request.POST.get('warning')
        cdn = request.POST.get("cdn")
        domain = request.POST.get("domain")
        print(domain)
        if domain == '':
            except_data['data'] = '请输入域名!'
            return HttpResponse(json.dumps(except_data))

        project_name = request.POST.get('project').strip()
        print(project_name)
        if project_name == '选择项目' or project_name == '':
            except_data['data'] = '请输入或选择项目!'
            return HttpResponse(json.dumps(except_data))


        nodes = json.loads(request.POST.get("nodes"))
        if Project.objects.filter(name=project_name).count() == 0:
            Project.objects.create(name=project_name)

        project_obj = Project.objects.get(name=project_name)
        for i in domain.split():
            if  DomainName.objects.filter(url=i).count() >= 1:
                except_data['data'] = '{} 已存在'.format(i)
                return HttpResponse(json.dumps(except_data))
        for i in domain.split():
            DomainName.objects.create(url=i, project_name_id=project_obj.id, check_id=check_id, warning=warning, cdn=cdn)
            domain_obj = DomainName.objects.get(url=i)
            domain_obj.nodes.add(*nodes)
        success_data['data'] = '新增成功'
    return HttpResponse(json.dumps(success_data))

# 更新域名状态页面的曲线图
@check_login
def update_graph(request):
    """
    更新曲线图
    :param request:
    :return:
        返回实时的曲线图数据
    """
    if request.method == 'POST':
        url_id = request.POST.get('url_id')
        defaultDomainData, graph_data = get_areas_data(url_id)
        return HttpResponse(json.dumps(graph_data))


# "域名状态"页的域名搜索
@check_login
def search(request):
    """
    搜索函数
    :param request:
    :return:
    """
    if request.method == 'POST':
        url = request.POST.get('url')
        url_obj = DomainName.objects.filter(url=url).first()

        if url_obj is None:
            return HttpResponse('no')
        else:
            return HttpResponse(url_obj.id)

# "域名管理"页面
@check_login
def tables(request,page=1):
    if request.method == 'GET':
        Domain_table_obj = Domain_table()
        domainall = Domain_table_obj.domain_all().order_by('project_name')
        paginator = Paginator(domainall, 20)
        try:
            one_page = paginator.page(page)
        except PageNotAnInteger:
            one_page = paginator.page(1)
        except EmptyPage:
            one_page = paginator.page(paginator.num_pages)

        data = {
            'project_all':Domain_table_obj.project_all(),
            'node':Node.objects.all(),
            'fault_number':Domain_table_obj.fault_number(),
            'domainall':one_page,
            'Not_check_number':Domain_table_obj.Not_check_number(),
            'lt_10':Domain_table_obj.lt_10(),
            'paginator':paginator
        }

    return render(request,'webmoni_tables.html',{'data':data})


# 项目筛选
@check_login
def tables_project(request,project_id):
    if request.method == 'GET':
        Domain_table_obj = Domain_table()
        data = {
            'project_all':Domain_table_obj.project_all(),
            'node': Node.objects.all(),
            'fault_number':Domain_table_obj.fault_number(),
            'domainall':Domain_table_obj.domain_all(project_id),
            'Not_check_number':Domain_table_obj.Not_check_number(),
            'lt_10':Domain_table_obj.lt_10()
        }
    return render(request,'webmoni_tables.html',{'data':data})


# 编辑域名
@check_login
def tables_edit(request):
    if request.method == "POST":
        url_id = request.POST.get('id')
        nodes = json.loads(request.POST.get('nodes'))
        check_id = request.POST.get('check_id')
        warning = request.POST.get('warning')
        cdn = request.POST.get("cdn")
        domain = request.POST.get("domain")

        if domain == '':
            except_data['data'] = '请输入域名!'
            return HttpResponse(json.dumps(except_data))

        project_name = request.POST.get('project').strip()
        print(project_name)
        if project_name == '选择项目' or project_name == '':
            except_data['data'] = '请输入或选择项目!'
            return HttpResponse(json.dumps(except_data))

        print(url_id, domain, check_id, warning, cdn, nodes)
        if Project.objects.filter(name=project_name).count() == 0:
            Project.objects.create(name=project_name)

        project_obj = Project.objects.get(name=project_name)
        DomainName.objects.filter(id=url_id).update(url=domain, project_name_id=project_obj.id, check_id=check_id, warning=warning,
                                  cdn=cdn)
        domain_obj = DomainName.objects.get(url=domain)
        domain_obj.nodes.set(nodes)

        success_data['data'] = '修改成功'
        return HttpResponse(json.dumps(success_data))

    if request.method == 'GET':
        url_id = request.GET.get('id')
        domain_info = DomainName.objects.get(id=url_id)
        success_data['data'] = {
            'domain_info':model_to_dict(domain_info),
        }
        return HttpResponse(json.dumps(success_data))

# 故障域名
@check_login
def tables_fault(request):
    if request.method == 'GET':
        Domain_table_obj = Domain_table()
        data = {
            'project_all':Domain_table_obj.project_all(),
            'node': Node.objects.all(),
            'fault_number':Domain_table_obj.fault_number(),
            'domainall':Domain_table_obj.fault_domain_obj(),
            'Not_check_number':Domain_table_obj.Not_check_number(),
            'lt_10': Domain_table_obj.lt_10()
        }
    return render(request,'webmoni_tables.html',{'data':data})

# 不检测的域名
@check_login
def tables_notcheck(request):
    if request.method == 'GET':
        Domain_table_obj = Domain_table()
        data = {
            'project_all':Domain_table_obj.project_all(),
            'node': Node.objects.all(),
            'fault_number':Domain_table_obj.fault_number(),
            'domainall':Domain_table_obj.DomainName.objects.filter(check_id=1),
            'Not_check_number':Domain_table_obj.Not_check_number(),
            'lt_10': Domain_table_obj.lt_10()
        }
    return render(request,'webmoni_tables.html',{'data':data})


# 证书即将过期的域名
@check_login
def tables_lt_10(request):
    if request.method == 'GET':
        Domain_table_obj = Domain_table()
        data = {
            'project_all':Domain_table_obj.project_all(),
            'fault_number':Domain_table_obj.fault_number(),
            'node': Node.objects.all(),
            'domainall':Domain_table_obj.DomainName.objects.filter(cert_valid_days__lt=10),
            'Not_check_number':Domain_table_obj.Not_check_number(),
            'lt_10': Domain_table_obj.lt_10()
        }
    return render(request,'webmoni_tables.html',{'data':data})

# 域名搜索
@check_login
def tables_search(request,url_id=None):
    if request.method == 'POST':
        url = request.POST.get('url')
        url_obj = DomainName.objects.filter(url=url).first()
        if url_obj is None:
            return HttpResponse('no')
        else:
            return HttpResponse(url_obj.id)

    if request.method == 'GET':
        if url_id is None:
            return  redirect('/webmoni/tables/')
        else:
            Domain_table_obj = Domain_table()
            data = {
                'project_all': Domain_table_obj.project_all(),
                'fault_number': Domain_table_obj.fault_number(),
                'domainall': Domain_table_obj.DomainName.objects.filter(id=url_id),
                'Not_check_number': Domain_table_obj.Not_check_number(),
                'lt_10': Domain_table_obj.lt_10()
            }
        return render(request, 'webmoni_tables.html', {'data': data})

# 域名删除
@check_login
def tables_delete(request):
    if request.method == "POST":
        url_id = request.POST.get('url_id')
        DomainName.objects.filter(id=url_id).delete()
        return HttpResponse('OK')

@check_login
# 更新证书有效期
def tables_update_cert(request):
    if request.method == 'POST':
        url_id = request.POST.get('url_id')
        domain = DomainName.objects.get(id=url_id)
        print(11,domain)
        msg = {
            'pattern':1,
            'domain':domain.url
        }
        launcher = Redis_Queue(Webmoni_Check_Cert_Queue)
        launcher.publish(msg)
        success_data['data'] = '已加入检测队列'
        return HttpResponse(json.dumps(success_data))

@check_login
def tables_update_all_cert(request):
    if request.method == 'POST':
        now = request.POST.get('now')
        last_check_all_cert_time = 0
        if  redis_conn.get('last_check_all_cert_time') is not None:
            last_check_all_cert_time = redis_conn.get('last_check_all_cert_time').decode()
        now_time = int(time.time())
        if now_time - int(last_check_all_cert_time) > 7200:
            msg = {
                'pattern': 0,
            }
            launcher = Redis_Queue(Webmoni_Check_Cert_Queue)
            launcher.publish(msg)
            redis_conn.set('last_check_all_cert_time',now_time)
            success_data['data'] = '开始更新'
            return HttpResponse(json.dumps(success_data))
        else:
            except_data['data'] = '请勿频繁更新所有证书信息,冷却时间2小时!'
            return HttpResponse(json.dumps(except_data))




# 节点管理页面
@check_login
def nodes(request):
    if request.method == 'GET':

        nodeFormsObj = NodeForms()
        node_all = Node.objects.all()
    return render(request,'webmoni_nodes.html',{'node_all':node_all,'nodeFormsObj':nodeFormsObj})

# 创建节点
@check_login
def nodes_create(request):
    if request.method == "POST":
        nodeFormsObj = NodeForms(request.POST)
        if nodeFormsObj.is_valid():
            Node.objects.create(**nodeFormsObj.clean())
        else:
            errors = nodeFormsObj.errors
            print(errors)
        return redirect('/webmoni/nodes/')


# 删除节点
@check_login
def nodes_delete(request):
    if request.method == "POST":
        node_id = request.POST.get('del_node')
        Node.objects.filter(id=node_id).delete()
        return redirect('/webmoni/nodes/')

# 日志展示页面
@check_login
def log(request,days=1,page=1):
    if request.method == 'GET':
        today = datetime.datetime.now().replace(hour=0,minute=0, second=0)
        stop_data = today - datetime.timedelta(days=int(days))
        log_all = Event_Log.objects.filter(datetime__gt=stop_data).order_by('-id')
        paginator = Paginator(log_all,20)
        try:
            one_page = paginator.page(page)
        except PageNotAnInteger:
            one_page = paginator.page(1)
        except EmptyPage:
            one_page = paginator.page(paginator.num_pages)

        data = {
            'paginator':paginator,
            'one_page':one_page,
            'days':days
        }
        return render(request,'webmoni_log.html',{'data':data})


def Nowarning(request,domain):
    if request.method == 'GET':
        try:
            DomainName.objects.filter(url=domain).update(warning=1)
            return HttpResponse('success')
        except Exception:
            return HttpResponse('失败,请查看系统日志!')

