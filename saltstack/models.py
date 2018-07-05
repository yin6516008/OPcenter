from django.db import models
# Create your models here.

class Project(models.Model):
    name = models.CharField(max_length=32,unique=True,null=True,blank=True)
    # def __str__(self):
    #     return self.name

class Accepted_minion(models.Model):
    salt_id = models.AutoField(primary_key=True)
    id = models.CharField(max_length=60,unique=True,null=False)
    project = models.ForeignKey('Project',to_field='id',null=True)
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
