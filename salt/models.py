from django.db import models
from webmoni.models import Node
# Create your models here.

class Node_Info(models.Model):
    node_id = models.IntegerField()
    node_name = models.CharField(max_length=20,unique=True)
    node_ip = models.CharField(max_length=20,null=True)
    salt_id = models.CharField(max_length=40,null=True)
    os_type = models.CharField(max_length=40,null=True)

