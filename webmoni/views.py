from django.shortcuts import render,redirect,HttpResponse
from django.db.models import Q
from django.forms.models import model_to_dict
from webmoni.models import MonitorData
from webmoni.models import DomainName
from webmoni.models import Project
from webmoni.models import Node
from webmoni.models import Event_Log
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from genericFunc import check_login
import datetime
import json

# 导入通用的函数
from webmoni.publicFunc import get_areas_data,Domain_table
from OPcenter.settings import webmoni_error_trigger

# Create your views here

@check_login
def areas(request,url_id=None):
    """
    区域展示页面
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
        return render(request,'show_areas.html',{'project_list':project_list,
                                                 'defaultDomainData':defaultDomainData,
                                                 'graph_data':graph_data})


@check_login
def create(request):
    """
    新建域名函数
    :param request:
    :return:
    """
    if request.method == 'POST':
        check_id = 0 if request.POST.get('check_id') is None else 1
        warning = 0 if request.POST.get('warning') is None else 1

        if request.POST.get('project'):
            project_id = request.POST.get('project')
            if request.POST.get('domain'):
                domain = request.POST.get('domain')
                DomainName.objects.create(url=domain,project_name_id=project_id,check_id=check_id,warning=warning)
            if request.POST.get('domains'):
                domains = request.POST.get('domains')
                for i in domains.split('\r\n'):
                    DomainName.objects.create(url=i, project_name_id=project_id,check_id=check_id,warning=warning)

        if request.POST.get('new_project'):
            project_name = request.POST.get('new_project')
            Project.objects.create(name=project_name)
            new_project = Project.objects.filter(name=project_name).first()
            if request.POST.get('domain'):
                domain = request.POST.get('domain')
                DomainName.objects.create(url=domain, project_name_id=new_project.id,check_id=check_id,warning=warning)
            if request.POST.get('domains'):
                domains = request.POST.get('domains')
                for i in domains.split('\r\n'):
                    DomainName.objects.create(url=i, project_name_id=new_project.id,check_id=check_id,warning=warning)
    return redirect('/webmoni/areas/')


@check_login
def delete(request):
    """
    删除域名函数
    :param request:
    :return:
    """
    if request.method == 'POST':
        id = request.POST.get('del_id')
        DomainName.objects.filter(id=id).delete()
    return redirect('/webmoni/areas/')



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

@check_login
def update_domain(request):
    if request.method == 'POST':
        domain_id = request.POST.get('domain')
        check_id = 0 if request.POST.get('check_id') is None else 1
        warning = 0 if request.POST.get('warning') is None else 1
        DomainName.objects.filter(id=domain_id).update(check_id=check_id,warning=warning)


        return redirect('/webmoni/areas-' + domain_id + '/')

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

@check_login
def tables(request,page=1):
    if request.method == 'GET':
        Domain_table_obj = Domain_table()
        domainall = Domain_table_obj.domain_all()
        paginator = Paginator(domainall, 20)
        try:
            one_page = paginator.page(page)
        except PageNotAnInteger:
            one_page = paginator.page(1)
        except EmptyPage:
            one_page = paginator.page(paginator.num_pages)

        data = {
            'project_all':Domain_table_obj.project_all(),
            'fault_number':Domain_table_obj.fault_number(),
            'domainall':one_page,
            'Not_check_number':Domain_table_obj.Not_check_number(),
            'lt_10':Domain_table_obj.lt_10(),
            'paginator':paginator
        }

    return render(request,'domain_table.html',{'data':data})

@check_login
def tables_project(request,project_id):
    if request.method == 'GET':
        Domain_table_obj = Domain_table()
        data = {
            'project_all':Domain_table_obj.project_all(),
            'fault_number':Domain_table_obj.fault_number(),
            'domainall':Domain_table_obj.domain_all(project_id),
            'Not_check_number':Domain_table_obj.Not_check_number(),
            'lt_10':Domain_table_obj.lt_10()

        }
    return render(request,'domain_table.html',{'data':data})

@check_login
def tables_edit(request):
    if request.method == "POST":
        try:
            url_id = request.POST.get('url_id')
            check_id = request.POST.get('check_id')
            warning = request.POST.get('warning')
            DomainName.objects.filter(id=url_id).update(check_id=check_id,warning=warning)
            return HttpResponse('true')
        except Exception:
            return HttpResponse('false')



@check_login
def tables_fault(request):
    if request.method == 'GET':
        Domain_table_obj = Domain_table()
        data = {
            'project_all':Domain_table_obj.project_all(),
            'fault_number':Domain_table_obj.fault_number(),
            'domainall':Domain_table_obj.fault_domain_obj(),
            'Not_check_number':Domain_table_obj.Not_check_number(),
            'lt_10': Domain_table_obj.lt_10()
        }
    return render(request,'domain_table.html',{'data':data})

@check_login
def tables_notcheck(request):
    if request.method == 'GET':
        Domain_table_obj = Domain_table()
        data = {
            'project_all':Domain_table_obj.project_all(),
            'fault_number':Domain_table_obj.fault_number(),
            'domainall':Domain_table_obj.DomainName.objects.filter(check_id=1),
            'Not_check_number':Domain_table_obj.Not_check_number(),
            'lt_10': Domain_table_obj.lt_10()
        }
    return render(request,'domain_table.html',{'data':data})

@check_login
def tables_lt_10(request):
    if request.method == 'GET':
        Domain_table_obj = Domain_table()
        data = {
            'project_all':Domain_table_obj.project_all(),
            'fault_number':Domain_table_obj.fault_number(),
            'domainall':Domain_table_obj.DomainName.objects.filter(cert_valid_days__lt=10),
            'Not_check_number':Domain_table_obj.Not_check_number(),
            'lt_10': Domain_table_obj.lt_10()
        }
    return render(request,'domain_table.html',{'data':data})

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
        return render(request, 'domain_table.html', {'data': data})


@check_login
def tables_delete(request):
    if request.method == "POST":
        url_id = request.POST.get('url_id')
        DomainName.objects.filter(id=url_id).delete()
        return HttpResponse('OK')


@check_login
def nodes(request):
    if request.method == 'GET':
        node_all = Node.objects.all()

    return render(request,'node_management.html',{'node_all':node_all})


@check_login
def nodes_create(request):
    if request.method == "POST":
        node_name = request.POST.get('node_name')
        node_ip = request.POST.get('node_ip')
        node_description = request.POST.get('node_description')
        Node.objects.create(node=node_name,ip=node_ip,description=node_description)
        return redirect('/webmoni/nodes/')

@check_login
def nodes_delete(request):
    if request.method == "POST":
        node_id = request.POST.get('del_node')
        Node.objects.filter(id=node_id).delete()
        return redirect('/webmoni/nodes/')

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