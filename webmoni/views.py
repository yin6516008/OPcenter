from django.shortcuts import render,redirect,HttpResponse
from django.db.models import Q
from django.forms.models import model_to_dict
from webmoni.models import MonitorData
from webmoni.models import DomainName
from webmoni.models import Project
from webmoni.models import Node
import datetime
import json

# 导入通用的函数
from webmoni.publicFunc import get_areas_data


# Create your views here


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

def update_domain(request):
    if request.method == 'POST':
        domain_id = request.POST.get('domain')
        check_id = 0 if request.POST.get('check_id') is None else 1
        warning = 0 if request.POST.get('warning') is None else 1
        DomainName.objects.filter(id=domain_id).update(check_id=check_id,warning=warning)
        print(domain_id,check_id,warning)

        return redirect('/webmoni/areas-' + domain_id + '/')


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


def tables(request):
    return render(request,'show_quality.html')