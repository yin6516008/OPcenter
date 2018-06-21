from django.db import models

# Create your models here.

class User(models.Model):
    user_name = models.CharField(max_length=20,unique=True,)
    password = models.CharField(max_length=200,)
    online_status_list = (
        ('Online','在线'),
        ('Offline','离线'),
        ('Exception','异常')
    )
    online_status = models.CharField(max_length=20,choices=online_status_list,default='Offline')
    def __str__(self):
        return self.user_name