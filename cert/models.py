from django.db import models

# Create your models here.

class Cert_info(models.Model):
    domain = models.CharField(max_length=100,unique=True)
    create_time = models.IntegerField()
    expire_time = models.IntegerField()
