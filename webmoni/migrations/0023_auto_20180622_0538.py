# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-06-22 05:38
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('webmoni', '0022_auto_20180621_1800'),
    ]

    operations = [
        migrations.AlterField(
            model_name='domainname',
            name='status',
            field=models.ForeignKey(default=100, null=True, on_delete=django.db.models.deletion.CASCADE, to='webmoni.Event_Type'),
        ),
    ]