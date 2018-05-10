from webmoni.models import *
from django.db.models import Q
import datetime

def get_areas_data(url_id):
    # 如果没选择域名,默认展示第一条域名
    if url_id is None:
        defaultDomain = DomainName.objects.first()
    else:
        # 如果选择了域名,就拿到选择的域名
        defaultDomain = DomainName.objects.filter(id=url_id).first()
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
        for i in range(0, 12):
            stop_time = start_time - datetime.timedelta(minutes=5)
            if len(time_list) < 12:
                time_list.insert(0, stop_time.strftime('%H:%M'))
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
                    node_data['values'].insert(0, time_node_data.total_time)
            else:
                node_data['values'].insert(0, '')
            start_time = stop_time
        data.append(node_data)
    graph_data = {
        'id': defaultDomain.id,
        'status': defaultDomain.status.event_type,
        'domain': defaultDomain.url,
        'time_list': time_list,
        'data': data
    }

    return  defaultDomainData,graph_data

