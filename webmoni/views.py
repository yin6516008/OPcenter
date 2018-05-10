from django.shortcuts import render,redirect,HttpResponse
from django.db.models import Q
from django.forms.models import model_to_dict
from webmoni.models import MonitorData
from webmoni.models import DomainName
from webmoni.models import Project
from webmoni.models import Node
import datetime
import json

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
    if request.method == 'POST':
        if request.POST.get('project'):
            project_id = request.POST.get('project')
            if request.POST.get('domain'):
                domain = request.POST.get('domain')
                DomainName.objects.create(url=domain,project_name_id=project_id)
            if request.POST.get('domains'):
                domains = request.POST.get('domains')
                for i in domains.split('\r\n'):
                    DomainName.objects.create(url=i, project_name_id=project_id)

        if request.POST.get('new_project'):
            project_name = request.POST.get('new_project')
            Project.objects.create(name=project_name)
            new_project = Project.objects.filter(name=project_name).first()
            if request.POST.get('domain'):
                domain = request.POST.get('domain')
                DomainName.objects.create(url=domain, project_name_id=new_project.id)
            if request.POST.get('domains'):
                domains = request.POST.get('domains')
                for i in domains.split('\r\n'):
                    DomainName.objects.create(url=i, project_name_id=new_project.id)
    return redirect('/webmoni/areas/')



def delete(request):
    if request.method == 'POST':
        id = request.POST.get('del_id')
        DomainName.objects.filter(id=id).delete()
    return redirect('/webmoni/areas/')




def update(request):
    if request.method == 'POST':
        url_id = request.POST.get('url_id')
        defaultDomainData, graph_data = get_areas_data(url_id)
        return HttpResponse(json.dumps(graph_data))