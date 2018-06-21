from django.contrib import admin

# Register your models here.

from webmoni.models import Project,DomainName,Event_Type

class ProjectAdmin(admin.ModelAdmin):
    list_display = ['id','name']

class DomainNameAdmin(admin.ModelAdmin):
    list_display = ['id','url','status','check_id','warning']

admin.site.register(Project,ProjectAdmin)
admin.site.register(DomainName,DomainNameAdmin)
admin.site.register(Event_Type)