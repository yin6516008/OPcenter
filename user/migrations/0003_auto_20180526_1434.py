# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-05-26 14:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20180526_1433'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='online_status',
            field=models.CharField(choices=[('Online', '在线'), ('Offline', '离线'), ('Exception', '异常')], default='Offline', max_length=20),
        ),
    ]
