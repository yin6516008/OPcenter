from django.conf.urls import url
from saltstack import views

urlpatterns = [
    # 主机管理
    url(r'^$', views.salt_minions),
    url(r'^minion_list/$', views.salt_minions),
    url(r'^minion_list/(\d+)/$', views.salt_minions),
    url(r'^minion_add/$', views.minion_add),
    url(r'^minion_test/$', views.minion_test),
    url(r'^minion_del/$', views.minion_del),
    url(r'^minion_search/$', views.minion_search),
    url(r'^minion_search/(\d+)/$', views.minion_search),
    # 剧本管理和操作
    url(r'^playbook/$', views.playbook),
    url(r'^playbook/(.*)/$', views.playbook_project),
    url(r'^playbook_upload/$', views.playbook_upload),
    url(r'^playbook_edit/$', views.playbook_edit),
    url(r'^playbook_save/$', views.playbook_save),
    url(r'^playbook_del/$', views.playbook_del),
    url(r'^playbook_exe/$', views.playbook_exe),
    url(r'^playbook_exe/(.*)/$', views.playbook_exe_project),
    url(r'^playbook_exe_sls/$', views.playbook_exe_sls),
    # 远程终端

]