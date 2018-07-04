from django.conf.urls import url
from webmoni import views
from webmoni import api

urlpatterns = [
    url(r'^$', views.areas),
    url(r'^areas/$', views.areas),
    url(r'^areas-(\d*)/$', views.areas),
    url(r'^create/$', views.create),
    url(r'^update_graph/$', views.update_graph),
    url(r'^search/$', views.search),
    url(r'^api/domain_all/$', api.domain_all),
    url(r'^api/event_type/$', api.event_type),
    url(r'^api/check_result_submit/$', api.check_result_submit),
    url(r'^tables/$', views.tables),
    url(r'^tables/(\d+)/$', views.tables),
    url(r'^tables/edit/$', views.tables_edit),
    url(r'^tables/fault/$', views.tables_fault),
    url(r'^tables/notcheck/$', views.tables_notcheck),
    url(r'^tables/lt_10/$', views.tables_lt_10),
    url(r'^tables/search/$', views.tables_search),
    url(r'^tables/search-(\d+)/$', views.tables_search),
    url(r'^tables/p/(\d+)/$', views.tables_project),
    url(r'^tables/delete/$', views.tables_delete),
    url(r'^tables/update_cert/$', views.tables_update_cert),
    url(r'^tables/update_all_cert/$', views.tables_update_all_cert),
    url(r'^nodes/$', views.nodes),
    url(r'^nodes/create/$', views.nodes_create),
    url(r'^nodes/delete/$', views.nodes_delete),
    url(r'^log/$', views.log),
    url(r'^log/(\d+)/(\d+)/$', views.log)
]