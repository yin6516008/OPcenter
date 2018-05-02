from django.conf.urls import url
from webmoni import views

urlpatterns = [
    url(r'^$', views.areas),
    url(r'^areas/', views.areas),
]