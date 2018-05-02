from django.db import models

# Create your models here.

class Node(models.Model):
    node = models.CharField(max_length=20,unique=True)

class DomainName(models.Model):
    url = models.CharField(max_length=60,unique=True)

class MonitorData(models.Model):
    node = models.ForeignKey('Node')
    url = models.ForeignKey('DomainName')
    http_code = models.IntegerField(null=True, default=None)
    namelookup_time = models.FloatField(null=True,default=None)
    connect_time = models.FloatField(null=True,default=None)
    pretransfer_time = models.FloatField(null=True,default=None)
    starttransfer_time = models.FloatField(null=True,default=None)
    total_time = models.FloatField(null=True,default=None)
    size_download = models.IntegerField(null=True,default=None)
    header_size = models.IntegerField(null=True,default=None)
    speed_download = models.IntegerField(null=True,default=None)
    datetime = models.DateTimeField()

class Event_Log(models.Model):
    node = models.ForeignKey('Node')
    url = models.ForeignKey('DomainName')
    event_type = models.ForeignKey('Event_Type')

class Event_Type(models.Model):
    event_type = models.CharField(max_length=60,unique=True)
