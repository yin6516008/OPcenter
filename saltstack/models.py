from django.db import models
# Create your models here.

class Project(models.Model):
    name = models.CharField(max_length=32,unique=True,null=True,blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "主机组"

class Accepted_minion(models.Model):
    status_choice = (
        (0,'离线'),
        (1,'在线'),
        (2,'检测中'),

    )
    salt_id = models.AutoField(primary_key=True)
    id = models.CharField(max_length=60,unique=True,null=False)
    status = models.IntegerField(choices=status_choice,null=True,blank=True)
    ipv4 = models.CharField(max_length=60,null=True,blank=True)
    city = models.CharField(max_length=20,null=True,blank=True)
    osfinger = models.CharField(max_length=60,null=True,blank=True)
    cpu_model = models.CharField(max_length=60,null=True,blank=True)
    num_cpus = models.IntegerField(null=True,blank=True)
    mem_total = models.IntegerField(null=True,blank=True)
    mem_gib = models.CharField(max_length=10,null=True, blank=True)
    datetime = models.DateTimeField()
    project = models.ManyToManyField('Project')

    def __str__(self):
        return self.id
    class Meta:
        verbose_name_plural = "主机列表"

class PlayBook(models.Model):
    playbook_stauts = (
        (0,'禁用'),
        (1,'可用'),
    )
    project = models.ForeignKey('Project')
    applied_file = models.CharField(max_length=100,null=True,blank=True)
    sls = models.CharField(max_length=100, null=True, blank=True)
    description = models.CharField(max_length=28,null=True,blank=True)
    status = models.IntegerField(choices=playbook_stauts,default=1)

    def __str__(self):
        return self.description

    class Meta:
        verbose_name_plural = "剧本"

class Async_jobs(models.Model):
    async_jobs_stauts = (
        (0,'排队中'),
        (1,'执行中'),
        (2,'已完成'),
        (3,'异常'),
    )
    jid = models.CharField(max_length=20,null=True,blank=True)
    number = models.CharField(max_length=11, unique=True, null=False)
    description = models.ForeignKey('PlayBook')
    project = models.ForeignKey('Project')
    minion = models.ManyToManyField('Accepted_minion')
    create_time = models.DateTimeField()
    start_time = models.DateTimeField(null=True,blank=True)
    finish_time = models.DateTimeField(null=True,blank=True)
    information = models.TextField(null=True,blank=True)
    status = models.IntegerField(choices=async_jobs_stauts,default=0)
    success_total = models.IntegerField(null=True,blank=True)
    targets_total = models.IntegerField(null=True,blank=True)
