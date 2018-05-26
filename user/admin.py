from django.contrib import admin

# Register your models here.
from user.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ['id','user_name','online_status']


admin.site.register(User,UserAdmin)