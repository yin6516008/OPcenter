from django.contrib import admin

# Register your models here.

from webmoni.models import Project,DomainName,Event_Type

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
    ordering = ('id',)


