"""
网站监控API  给数据采集器用来增删查改数据库用,调用前需要检测数据采集器是否合法。
"""
from django.shortcuts import render,redirect,HttpResponse
from django.db.models import Q
from django.forms.models import model_to_dict
from webmoni.models import MonitorData
from webmoni.models import DomainName
from webmoni.models import Project
from webmoni.models import Node
from webmoni.models import Event_Type
from webmoni.models import Event_Log
from webmoni.models import MonitorData

from webmoni.publicFunc import API_verify
import datetime
import json


def domain_all(request):
    if request.method == 'POST':
        data = {}

        node_id = request.POST.get('node')
        client_ip = request.META['REMOTE_ADDR']
        if API_verify(node_id,client_ip):
            data['status'] = 'OK'
            data['data'] = list(DomainName.objects.all().values())
            return HttpResponse(json.dumps(data))
        else:
            data['status'] = 'error'
            return HttpResponse(json.dumps(data))
    if request.method == 'GET':
        return HttpResponse('连接拒绝')


def event_type(request):
    if request.method == 'POST':
        data = {}

        node_id = request.POST.get('node')
        client_ip = request.META['REMOTE_ADDR']
        if API_verify(node_id,client_ip):
            data['status'] = 'OK'
            data['data'] = list(Event_Type.objects.all().values())
            return HttpResponse(json.dumps(data))
        else:
            data['status'] = 'error'
            return HttpResponse(json.dumps(data))
    if request.method == 'GET':
        return HttpResponse('连接拒绝')



def normal_domain(request):
    if request.method == 'POST':

        normalData = json.loads(request.POST.get('normalData'))
        print(normalData['data'])
        client_ip = request.META['REMOTE_ADDR']
        if API_verify(normalData.get('node'),client_ip):
            MonitorData.objects.create(**normalData['data'])
            return HttpResponse('OK')
        else:
            return HttpResponse('出错啦')
    if request.method == 'GET':
        return HttpResponse('连接拒绝')


def fault_domain(request):
    if request.method == 'POST':

        faultData = json.loads(request.POST.get('faultData'))
        print(faultData['data'])
        client_ip = request.META['REMOTE_ADDR']
        if API_verify(faultData.get('node'),client_ip):
            MonitorData.objects.create(**faultData['data'])
            DomainName.objects.filter(id=faultData['url_id']).update(**faultData['domain'])
            Event_Log.objects.create(**faultData['event_log'])
            return HttpResponse('OK')
        else:
            return HttpResponse('ERROR')
    if request.method == 'GET':
        return HttpResponse('连接拒绝')

def cert_update(request):
    if request.method == 'POST':
        cert_info = json.loads(request.POST.get('cert_info'))
        print(cert_info['data'])
        client_ip = request.META['REMOTE_ADDR']
        if API_verify(cert_info.get('node'),client_ip):
            DomainName.objects.filter(id=cert_info['url_id']).update(**cert_info['data'])
            return HttpResponse('OK')
        else:
            return HttpResponse('ERROR')
    if request.method == 'GET':
        return HttpResponse('连接拒绝')