from django.db import models

# Create your models here.

class user(models.Model):
    user_name = models.CharField(max_length=20,unique=True,)
    password = models.CharField(max_length=200,)
    online_status = (
        ('Online','在线'),
        ('Offline','离线'),
        ('Exception','异常')
    )
    online = models.CharField(max_length=2,choices=online_status,default='Offline')
