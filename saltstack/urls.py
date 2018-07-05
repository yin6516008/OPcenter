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
    url(r'^controlcenter/$', views.control_center),
]