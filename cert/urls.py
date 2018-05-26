from django.conf.urls import url
from cert import views

urlpatterns = [
    url(r'^$', views.cert_list),
    url(r'^apply/$', views.cert_apply),

]