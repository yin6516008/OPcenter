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
        data = {}

        node_id = request.POST.get('node')
        client_ip = request.META['REMOTE_ADDR']
        if API_verify(node_id,client_ip):
            return HttpResponse('连接拒绝')

    if request.method == 'GET':
        return HttpResponse('连接拒绝')


