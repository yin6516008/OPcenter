from django.conf.urls import url
from webmoni import views
from webmoni import api

urlpatterns = [
    url(r'^$', views.areas),
    url(r'^areas/$', views.areas),
    url(r'^areas-(\d*)/$', views.areas),
    url(r'^create/$', views.create),
    url(r'^delete/$', views.delete),
    url(r'^update_graph/$', views.update_graph),
    url(r'^update_domain/$', views.update_domain),
    url(r'^search/$', views.search),
    url(r'^api/domain_all/$', api.domain_all),
    url(r'^api/event_type/$', api.event_type),
    url(r'^api/normal_domain/$', api.normal_domain),
    url(r'^api/fault_domain/$', api.fault_domain),
    url(r'^tables/$', views.tables),
    url(r'^tables/fault/$', views.tables_fault),
    url(r'^tables/notcheck/$', views.tables_notcheck),
    url(r'^tables/p/(\d+)/$', views.tables_project)
]