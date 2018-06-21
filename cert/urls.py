from django.conf.urls import url
from cert import views

urlpatterns = [
    url(r'^$', views.cert_list),
    url(r'^apply/$', views.cert_apply),
    url(r'^TrustAsia_apply/$', views.cert_TrustAsia_apply),
    url(r'^TrustAsia_apply/create_order/$', views.cert_TrustAsia_apply_create_order),
    url(r'^TrustAsia_apply/Order_Authz/$', views.cert_TrustAsia_apply_Order_Authz),
    url(r'^TrustAsia_apply/download/nginx/(.*)/$', views.cert_TrustAsia_download_nginx),
    url(r'^TrustAsia_apply/download/iis/(.*)/$', views.cert_TrustAsia_download_iis),
    url(r'^TrustAsia_order_list/$', views.TrustAsia_order_list),
    url(r'^TrustAsia_order_list/(\d+)/$', views.TrustAsia_order_list),
    url(r'^TrustAsia_cert_list/$', views.TrustAsia_cert_list),
    url(r'^TrustAsia_cert_delete/$', views.TrustAsia_cert_delete),
    url(r'^TrustAsia_cert_list/(\d+)/$', views.TrustAsia_cert_list),
    url(r'^TrustAsia_cert_detail/$', views.TrustAsia_cert_detail),
    url(r'^TrustAsia_cert_select/(.*)/$', views.TrustAsia_cert_select),
    url(r'^TrustAsia_order_detail/$', views.TrustAsia_order_detail),
    url(r'^TrustAsia_order_delete/$', views.TrustAsia_order_delete),
    url(r'^apply/postdomain/$', views.cert_apply_postdomain),
    url(r'^apply/genercert/$', views.cert_apply_genercert),
    url(r'^download/nginx/(.*)/$', views.cert_TrustAsia_download_nginx),
    url(r'^download/iis/(.*)/$', views.cert_TrustAsia_download_iis),
    url(r'^download/(.*)/(.*)/$', views.cert_download),
    url(r'^getfile/$', views.cert_getfile),
    url(r'^delete/$', views.cert_delete)

]