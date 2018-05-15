from django.conf.urls import url
from webmoni import views

urlpatterns = [
    url(r'^$', views.areas),
    url(r'^areas/', views.areas),
    url(r'^areas-(\d*)/', views.areas),
    url(r'^create/', views.create),
    url(r'^delete/', views.delete),
    url(r'^update_graph/', views.update_graph),
    url(r'^update_domain/', views.update_domain),
    url(r'^search/', views.search),
    url(r'^tables/', views.tables)
]