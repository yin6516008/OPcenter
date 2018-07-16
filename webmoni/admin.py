from django.contrib import admin

# Register your models here.

from webmoni.models import Project
from webmoni.models import DomainName
from webmoni.models import Event_Type
from webmoni.models import Node

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['id','name']
    ordering = ('id',)

@admin.register(DomainName)
class DomainNameAdmin(admin.ModelAdmin):
    ordering = ('id',)
    list_display_links = ['url']
    filter_horizontal = ['nodes',]

    list_display = ['id','url','project_name','status','check_id','warning','cert_valid_date','cert_valid_days',]

@admin.register(Event_Type)
class EventTypeAdmin(admin.ModelAdmin):
    list_display = ['id','event_type']
    list_display_links = ['event_type']
    ordering = ('id',)


@admin.register(Node)
class EventTypeAdmin(admin.ModelAdmin):
    list_display = ['id','node','ip','description','online']
    list_display_links = ['node']
    ordering = ('id',)
