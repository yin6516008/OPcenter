from django.shortcuts import render,redirect
from django.db.models import Q
from django.forms.models import model_to_dict
from webmoni.models import MonitorData
from webmoni.models import DomainName
from webmoni.models import Project
from webmoni.models import Node
import datetime


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

        # 如果没选择域名,默认展示第一条域名
        if url_id is None:
            defaultDomain = DomainName.objects.first()
        else:
            # 如果选择了域名,就拿到选择的域名
            defaultDomain = DomainName.objects.filter(id=url_id).first()
            print(defaultDomain.url)

        # 拿到所有的节点,通过节点去数据库查找数据,网站五分钟检测一次

        defaultNode = Node.objects.all().order_by('id')
        m = int(datetime.datetime.now().minute / 5) * 5
        show_start_time = datetime.datetime.now().replace(minute=m, second=0)
        defaultDomainData = []
        data = []
        time_list = []
        for row in defaultNode:
            start_time = show_start_time
            node_data = {
                'node': row.node,
                'values': []
            }
            for i in range(0,12):
                stop_time = start_time - datetime.timedelta(minutes=5)
                if len(time_list) < 12:
                    time_list.insert(0,stop_time.strftime('%H:%M'))
                time_node_data = row.monitordata_set.filter(Q(datetime__lte=start_time)
                                                            & Q(datetime__gt=stop_time)
                                                            & Q(url=defaultDomain.id)).first()
                if i == 0:
                    defaultDomainData.append(time_node_data)

                if time_node_data is not None:
                    if time_node_data.total_time is None:
                        print(time_node_data.total_time)
                        node_data['values'].insert(0, '')
                    else:
                        node_data['values'].insert(0,time_node_data.total_time)
                else:
                    node_data['values'].insert(0,'')
                start_time = stop_time
            data.append(node_data)
        graph_data = {
            'time_list': time_list,
            'data': data
        }
        return render(request,'show_areas.html',{'project_list':project_list,
                                                 'defaultDomainData':defaultDomainData,
                                                 'graph_data':graph_data})


def create(request):
    if request.method == 'POST':
        if request.POST.get('project'):
            project_id = request.POST.get('project')
            print(project_id)
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