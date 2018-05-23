from webmoni.models import *
from django.db.models import Q
import datetime

# 根据url_id获取网站监控--》域名状态页面的数据并返回
def get_areas_data(url_id):
    # 如果没选择域名,默认展示第一条域名
    if url_id is None:
        defaultDomain = DomainName.objects.first()
    else:
        # 如果选择了域名,就拿到选择的域名
        defaultDomain = DomainName.objects.filter(id=url_id).first()

    # 拿到上次5分种整的时间
    m = int(datetime.datetime.now().minute / 5) * 5
    # 起始时间
    start_time = datetime.datetime.now().replace(minute=m, second=0)
    # 结束时间
    stop_time = start_time - datetime.timedelta(hours=1)

    # 存放区域展示页面里表格的数据
    table_data = []
    # 存放区域展示页面里曲线图的数据
    data = []
    # 存放区域展示页面里曲线图时间的数据
    time_list =[]

    # 拿到所有的节点,通过节点去数据库查找数据,网站五分钟检测一次
    defaultNode = Node.objects.all().order_by('id')
    for row in defaultNode:
        # 用于存放一个节点数据
        node_data = {
            'node': row.node,
            'values': []
        }
        # 获取当前url一个小时以内的数据
        last_12 = row.monitordata_set.filter(Q(url=defaultDomain.id) &
            Q(datetime__lt=start_time) & Q(datetime__gte=stop_time)).order_by('datetime')

        print(len(last_12))
        print(last_12)

        # 表格只展示最后一次检测的数据
        if len(last_12) != 0:
            table_data.append(last_12.reverse()[0])

        # 把一个小时以内的数据分成12段,每五分钟一段,将数据存入node_data
        head = start_time
        for i in range(0,12):
            tail = head - datetime.timedelta(minutes=5)
            if len(time_list) < 12:
                time_list.insert(0,tail.strftime('%H:%M'))
            one_data = last_12.filter(Q(datetime__lt=head) & Q(datetime__gte=tail)).first()
            if one_data is None:
                node_data['values'].insert(0, '')
            else:
                node_data['values'].insert(0, '') if one_data.total_time is None else node_data['values'].insert(0, one_data.total_time)
            head = tail
        # 将一个区域的数据存入data
        data.append(node_data)

    graph_data = {
        'project':defaultDomain.project_name.name,
        'id': defaultDomain.id,
        'status': defaultDomain.status.event_type,
        'domain': defaultDomain.url,
        'check_id':defaultDomain.check_id,
        'warning':defaultDomain.warning,
        'time_list': time_list,
        'data': data
    }

    return  table_data,graph_data


# 获取主页 "网站监控统计" 图里的数据
def get_index_pie():
    ok_number = DomainName.objects.filter(status=100).filter(check_id=0).count()
    error_number = DomainName.objects.filter(~Q(status= 100)).filter(check_id=0).count()
    no_check = DomainName.objects.filter(~Q(check_id=0)).count()
    data = [
        {
            'value': ok_number,
            'name': '正常'
        },
        {
            'value':error_number,
            'name':'异常'
        },
        {
            'value':no_check,
            'name':'不检测'
        }
    ]
    return data

# webmoni APP的API验证方法,通过验证客户端IP,实现只有节点机器才能调用API
def API_verify(node_id,client_ip):
    if client_ip == '127.0.0.1':
        return True
    if node_id is None:
        return False
    node_obj = Node.objects.filter(id=node_id).first()
    if node_obj is None:
        return False
    return True if client_ip == node_obj.ip else False

