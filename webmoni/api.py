"""
网站监控API  给数据采集器用来增删查改数据库用,调用前需要检测数据采集器是否合法。
"""

from django.shortcuts import HttpResponse
from webmoni.models import Event_Type
from webmoni.models import Event_Log
from webmoni.models import MonitorData
from django.db.utils import  IntegrityError
from webmoni.publicFunc import API_verify
import json
from Aladdin.RedisQueue import Redis_Queue
from Aladdin.config import Webmoni_Send_Mail_Queue
from django.conf import settings

success_data = settings.SUCCESS_DATA
except_data = settings.EXCEPT_DATA





# /webmoni/api/domain_all/ 发送DomainName表数据
def domain_all(request):
    if request.method == 'POST':
        client_ip = request.META['REMOTE_ADDR']
        node_obj = API_verify(client_ip)
        if node_obj is not None:
            domains = node_obj.domainname_set.filter(check_id=0)
            success_data['data'] = list(domains.values())
            success_data['node'] = node_obj.id
            return HttpResponse(json.dumps(success_data))
        else:
            except_data['data'] = 'API验证失败'
            return HttpResponse(json.dumps(except_data))
    if request.method == 'GET':
        except_data['data'] = '拒绝GET请求'
        return HttpResponse(json.dumps(except_data))


# /webmoni/api/event_type/ 发送Event_Type表数据
def event_type(request):
    if request.method == 'POST':
        client_ip = request.META['REMOTE_ADDR']
        if API_verify(client_ip) is not None:
            success_data['data'] = list(Event_Type.objects.all().values())
            return HttpResponse(json.dumps(success_data))
        else:

            except_data['data'] = 'API验证失败'
            return HttpResponse(json.dumps(except_data))
    if request.method == 'GET':
        except_data['data'] = '拒绝GET请求'
        return HttpResponse(json.dumps(except_data))


# /webmoni/api/normal_domain/ 获取并保存正确的检测结果
def check_result_submit(request):
    if request.method == 'POST':
        submitData = json.loads(request.POST.get('submitData'))
        client_ip = request.META['REMOTE_ADDR']
        node_obj = API_verify(client_ip)
        if node_obj is not None:
            launcher = Redis_Queue(Webmoni_Send_Mail_Queue)
            try:
                MonitorData.objects.create(
                    http_code=submitData.get('http_code'),
                    total_time=submitData.get('total_time'),
                    datetime=submitData.get('datetime'),
                    node_id=submitData.get('node'),
                    url_id=submitData.get('url_id')
                )
                if not submitData.get('status') == 100:
                    Event_Log.objects.create(
                        datetime=submitData.get('datetime'),
                        event_type_id=submitData.get('status'),
                        node_id=submitData.get('node'),
                        url_id=submitData.get('url_id'),
                    )
                launcher.publish(submitData)
                success_data['data'] = '数据存储成功'
                return HttpResponse(json.dumps(success_data))
            except IntegrityError :
                except_data['data'] = 'IntegrityError 数据存储异常'
                return HttpResponse(json.dumps(except_data))
        else:
            except_data['data'] = 'API验证失败'
            return HttpResponse(json.dumps(except_data))
    if request.method == 'GET':
        except_data['data'] = '拒绝GET请求'
        return HttpResponse(json.dumps(except_data))
