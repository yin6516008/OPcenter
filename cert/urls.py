from django.conf.urls import url
from cert import views

urlpatterns = [
    url(r'^$', views.cert_list),
    url(r'^apply/$', views.cert_apply),
    url(r'^apply/postdomain/$', views.cert_apply_postdomain),
    url(r'^apply/genercert/$', views.cert_apply_genercert),
    url(r'^download/(.*)/(.*)/$', views.cert_download),
    url(r'^getfile/$', views.cert_getfile),
    url(r'^delete/$', views.cert_delete)

]