from django.db import models
from webmoni.models import Node
# Create your models here.

class Accepted_minion(models.Model):
    salt_id = models.AutoField(primary_key=True)
    id = models.CharField(max_length=60,unique=True,null=False)
    status = models.IntegerField(null=True,blank=True)
    ipv4 = models.CharField(max_length=60,null=True,blank=True)
    city = models.CharField(max_length=20,null=True,blank=True)
    osfinger = models.CharField(max_length=60,null=True,blank=True)
    cpu_model = models.CharField(max_length=60,null=True,blank=True)
    cpuarch = models.CharField(max_length=20,null=True,blank=True)
    num_cpus = models.IntegerField(null=True,blank=True)
    mem_total = models.IntegerField(null=True,blank=True)
    mem_gib = models.CharField(max_length=10,null=True, blank=True)
    datetime = models.DateTimeField()

# class Unaccepted_minion(models.Model):
#     salt_id = models.AutoField(primary_key=True)
#     id = models.CharField(max_length=60,unique=True,null=False)
#     ipv4 = models.CharField(max_length=60,null=True,blank=True)
#     city = models.CharField(max_length=20,null=True,blank=True)
#     datetime = models.DateTimeField()

# class Exception_minion(models.Model):
#     salt_id = models.AutoField(primary_key=True)
#     id = models.CharField(max_length=60,null=False)
#     exception = models.CharField(max_length=60,unique=True,null=False)
#     datetime = models.DateTimeField()