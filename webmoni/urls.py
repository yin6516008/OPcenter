from django.conf.urls import url
from webmoni import views

urlpatterns = [
    url(r'^$', views.areas),
    url(r'^areas/', views.areas),
    url(r'^areas-(\d*)/', views.areas),
    url(r'^create/', views.create),
    url(r'^delete/', views.delete),
    url(r'^update/', views.update),
]