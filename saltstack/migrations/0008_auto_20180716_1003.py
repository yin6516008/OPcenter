# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-07-16 10:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('saltstack', '0007_auto_20180714_1313'),
    ]

    operations = [
        migrations.AlterField(
            model_name='async_jobs',
            name='number',
            field=models.CharField(max_length=11, unique=True),
        ),
    ]
