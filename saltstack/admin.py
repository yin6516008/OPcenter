from django.contrib import admin

# Register your models here.
from saltstack.models import Project
from saltstack.models import Accepted_minion
from saltstack.models import PlayBook

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['id','name']


@admin.register(PlayBook)
class PlayBookAdmin(admin.ModelAdmin):
    list_display = ['project','applied_file','description','status']
    fk_fields = ('status')


@admin.register(Accepted_minion)
class Accepted_minionAdmin(admin.ModelAdmin):
    list_display = ['salt_id','id','status','ipv4','city','osfinger','datetime']
    list_display_links = ['id']
    filter_horizontal = ['project',]