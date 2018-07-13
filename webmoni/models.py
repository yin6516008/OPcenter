from django.db import models

# Create your models here.
class Node(models.Model):
    node = models.CharField(max_length=20,unique=True)
    ip = models.CharField(max_length=20,null=True)
    description = models.CharField(max_length=4096,null=True)
    online= models.IntegerField(null=True,default=None)

    def __str__(self):
        return self.node
    class Meta:
        verbose_name_plural = "节点"


class Project(models.Model):
    name = models.CharField(max_length=20,unique=True,null=True)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = "项目"

class DomainName(models.Model):
    url = models.CharField(max_length=60,unique=True)
    project_name = models.ForeignKey('Project',to_field='id',null=True)
    status = models.ForeignKey('Event_Type',to_field='id',null=True,default=100)
    cert_valid_date = models.CharField(null=True,max_length=20,default=None)
    cert_valid_days = models.IntegerField(null=True,default=None)
    check_id = models.IntegerField(default=0)
    warning = models.IntegerField(default=0)
    cdn = models.CharField(null=True,default=None,max_length=60)
    nodes = models.ManyToManyField('Node')
    def __str__(self):
        return self.url

    class Meta:
        verbose_name_plural = "域名信息"

class MonitorData(models.Model):
    node = models.ForeignKey('Node',to_field='id')
    url = models.ForeignKey('DomainName',to_field='id')
    http_code = models.IntegerField(null=True)
    total_time = models.IntegerField(null=True)
    datetime = models.DateTimeField(db_index=True)

class Event_Log(models.Model):
    node = models.ForeignKey('Node',to_field='id')
    url = models.ForeignKey('DomainName',to_field='id')
    event_type = models.ForeignKey('Event_Type',to_field='id')
    datetime = models.DateTimeField()

class Event_Type(models.Model):
    event_type = models.CharField(max_length=60,unique=True)
    def __str__(self):
        return self.event_type
    class Meta:
        verbose_name_plural = "事件类型"
