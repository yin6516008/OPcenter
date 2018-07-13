from django.conf.urls import url
from saltstack import views

urlpatterns = [
    url(r'^$', views.accepted_list),
    url(r'^minion_list/$', views.accepted_list),
    url(r'^minion_list/(\d+)/$', views.accepted_list),
    url(r'^minion_add/$', views.minion_add),
    url(r'^minion_test/$', views.minion_test),
    url(r'^minion_del/$', views.minion_del),
    url(r'^minion_search/$', views.minion_search),
    url(r'^minion_search/(\d+)/$', views.minion_search),

    url(r'^playbook/$', views.playbook),
    url(r'^playbook/(.*)/$', views.playbook_project),
    url(r'^playbook_upload/$', views.playbook_upload),
    url(r'^playbook_edit/$', views.playbook_edit),
    url(r'^playbook_save/$', views.playbook_save),
    url(r'^playbook_del/$', views.playbook_del),
    url(r'^playbook_exe/$', views.playbook_exe),
    url(r'^playbook_exe/(.*)/$', views.playbook_exe_project),

    url(r'^playbook_exe_sls/$', views.playbook_exe_sls),

    url(r'^master_manage/$', views.master_manage),
    url(r'^opcenter_slave_init/$', views.opcenter_slave_init),
    url(r'^opcenter_slave_release/$', views.opcenter_slave_release),

]