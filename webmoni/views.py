from django.shortcuts import render,redirect,HttpResponse
from django.db.models import Q
from django.forms.models import model_to_dict
from webmoni.models import MonitorData
from webmoni.models import DomainName
from webmoni.models import Project
from webmoni.models import Node
from webmoni.models import Event_Log

from genericFunc import check_login
import datetime
import json

# 导入通用的函数
from webmoni.publicFunc import get_areas_data


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
        print(domain_id,check_id,warning)

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
        print(url_obj)
        if url_obj is None:
            return HttpResponse('no')
        else:
            return HttpResponse(url_obj.id)

@check_login
def tables(request):
    if request.method == 'GET':
        project_all = Project.objects.all()
        domainall = DomainName.objects.all()
        fault_number = DomainName.objects.filter(~Q(status_id=0) & Q(check_id=0)).count()
        Not_check_number = DomainName.objects.filter(check_id=1).count()
        lt_30 = DomainName.objects.filter(cert_valid_days__lt=30).count()
        data = {
            'project_all':project_all,
            'fault_number':fault_number,
            'domainall':domainall,
            'Not_check_number':Not_check_number,
            'lt_30':lt_30
        }
    return render(request,'domain_table.html',{'data':data})

@check_login
def tables_project(request,project_id):
    if request.method == 'GET':
        project_all = Project.objects.all()
        domainall = DomainName.objects.filter(project_name=project_id)
        fault_number = DomainName.objects.filter(~Q(status_id=0) & Q(check_id=0)).count()
        Not_check_number = DomainName.objects.filter(check_id=1).count()
        lt_30 = DomainName.objects.filter(cert_valid_days__lt=30).count()
        data = {
            'project_all':project_all,
            'fault_number':fault_number,
            'domainall':domainall,
            'Not_check_number':Not_check_number,
            'lt_30':lt_30

        }
    return render(request,'domain_table.html',{'data':data})

@check_login
def tables_fault(request):
    if request.method == 'GET':
        project_all = Project.objects.all()
        domainall = DomainName.objects.filter(~Q(status_id=0) & Q(check_id=0))
        fault_number = DomainName.objects.filter(~Q(status_id=0) & Q(check_id=0)).count()
        Not_check_number = DomainName.objects.filter(check_id=1).count()
        lt_30 = DomainName.objects.filter(cert_valid_days__lt=30).count()
        data = {
            'project_all':project_all,
            'fault_number':fault_number,
            'domainall':domainall,
            'Not_check_number':Not_check_number,
            'lt_30': lt_30
        }
    return render(request,'domain_table.html',{'data':data})

@check_login
def tables_notcheck(request):
    if request.method == 'GET':
        project_all = Project.objects.all()
        domainall = DomainName.objects.filter(check_id=1)
        fault_number = DomainName.objects.filter(~Q(status_id=0) & Q(check_id=0)).count()
        Not_check_number = DomainName.objects.filter(check_id=1).count()
        lt_30 = DomainName.objects.filter(cert_valid_days__lt=30).count()
        data = {
            'project_all':project_all,
            'fault_number':fault_number,
            'domainall':domainall,
            'Not_check_number':Not_check_number,
            'lt_30': lt_30
        }
    return render(request,'domain_table.html',{'data':data})

@check_login
def tables_lt_30(request):
    if request.method == 'GET':
        project_all = Project.objects.all()
        domainall = DomainName.objects.filter(cert_valid_days__lt=30)
        fault_number = DomainName.objects.filter(~Q(status_id=0) & Q(check_id=0)).count()
        Not_check_number = DomainName.objects.filter(check_id=1).count()
        lt_30 = DomainName.objects.filter(cert_valid_days__lt=30).count()
        data = {
            'project_all':project_all,
            'fault_number':fault_number,
            'domainall':domainall,
            'Not_check_number':Not_check_number,
            'lt_30': lt_30
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
            project_all = Project.objects.all()
            domainall = DomainName.objects.filter(id=url_id)
            fault_number = DomainName.objects.filter(~Q(status_id=0) & Q(check_id=0)).count()
            Not_check_number = DomainName.objects.filter(check_id=1).count()
            lt_30 = DomainName.objects.filter(cert_valid_days__lt=30).count()
            data = {
                'project_all': project_all,
                'fault_number': fault_number,
                'domainall': domainall,
                'Not_check_number': Not_check_number,
                'lt_30': lt_30
            }
        return render(request, 'domain_table.html', {'data': data})


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
def log(request):
    if request.method == 'GET':
        log_all = Event_Log.objects.all()[0:100]
        return render(request,'webmoni_log.html',{'log_all':log_all})