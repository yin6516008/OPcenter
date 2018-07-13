# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-07-13 16:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('saltstack', '0002_playbook_sls'),
    ]

    operations = [
        migrations.RenameField(
            model_name='async_jobs',
            old_name='creationtime',
            new_name='create_time',
        ),
        migrations.RenameField(
            model_name='async_jobs',
            old_name='completiontime',
            new_name='start_time',
        ),
        migrations.AddField(
            model_name='async_jobs',
            name='duration',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='async_jobs',
            name='jid',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]