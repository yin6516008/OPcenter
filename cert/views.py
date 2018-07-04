from django.shortcuts import render,HttpResponse,redirect
# 导入ACME类
from cert.ACME_API import ACME_cll
import json,os
import time
from django.http import FileResponse
# Create your views here.
from login.AuthLogin import check_login
from cert.FreeSLL_API import TrustAsia
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

@check_login
def cert_list(request):
    """
    let's Encrypt证书列表
    :param request:
    :return:
    """
    acme_obj = ACME_cll()
    cert_info_list = acme_obj.getcertdir()
    if cert_info_list is None:
        return render(request,'cert_list.html',{'cert_dir':''})
    cert_dir = []
    for row in cert_info_list:
        cert_time = row.split()
        if len(cert_time)<2:
            cert_dir.append({'domain':cert_time[0],'valid_day':''})
            continue
        valid_day = int((int(cert_time[1]) + 90*3600*24 - time.time()) / (3600 * 24))
        cert_dir.append({'domain':cert_time[0],'valid_day':valid_day})
        print(cert_dir)
    return render(request,'cert_list.html',{
        'cert_dir':cert_dir
    })

@check_login
def cert_apply(request):
    """
    let's Encrypt证书申请页面
    :param request:
    :return:
    """
    return render(request,'cert_apply.html')


@check_login
def cert_apply_postdomain(request):
    """
    let's Encrypt生成TXT和主机记录
    :param request:
    :return:
    """
    if request.method == 'POST':
        domain = request.POST.get('domain')
        acme_obj = ACME_cll(domain)
        result = acme_obj.generTXT()
        return HttpResponse(json.dumps(result))


@check_login
def cert_apply_genercert(request):
    """
    let's Encrypt生成证书
    :param request:
    :return:
    """
    if request.method == 'POST':
        domain = request.POST.get('domain')
        acme_obj = ACME_cll(domain)
        result = acme_obj.generCert()
        print(result)
        return HttpResponse(json.dumps(result))

@check_login
def cert_download(request,domain,file):
    """
    let's Encrypt证书下载
    :param request:
    :param domain:
    :param file:
    :return:
    """
    if request.method == 'GET':
        file_path = domain + '/' + file
        acme_obj = ACME_cll(domain)
        file_abspath = acme_obj.cert_download(file_path)
        if os.path.exists(file_abspath):
            file_download = open(file_abspath,'rb')
            response = FileResponse(file_download)
            response['Content-Type'] = 'application/octet-stream'
            response['Content-Disposition'] = 'attachment;filename=%s'%file
            return response
        else:
            return redirect("/cert/apply/")

@check_login
def cert_getfile(request):
    """
    let's Encrypt获取证书文件
    :param request:
    :return:
    """
    if request.method == 'POST':
        domain = request.POST.get('domain')
        acme_obj = ACME_cll(domain)
        files = acme_obj.getcertfile()
        return HttpResponse(json.dumps(files))

@check_login
def cert_delete(request):
    """
    删除证书
    :param request:
    :return:
    """
    if request.method == 'POST':
        domain = request.POST.get('domain')
        acme_obj = ACME_cll(domain)
        resute = acme_obj.cert_delete()
        if resute:
            return HttpResponse('OK')
        else:
            return HttpResponse('ERROR')

@check_login
def cert_nginx_download(request,domain):
    """
    let's Encrypt下载nginx证书包
    :param request:
    :param domain:
    :return:
    """
    if request.method == 'GET':
        filename = 'nginx-'+domain+'.zip'
        file_abspath = '/root/.acme.sh/'+domain +'/' + filename
        if os.path.exists(file_abspath):
            file_download = open(file_abspath,'rb')
            response = FileResponse(file_download)
            response['Content-Type'] = 'application/octet-stream'
            response['Content-Disposition'] = 'attachment;filename=%s'%filename
            return response
        else:
            return redirect("/cert/apply/")

@check_login
def cert_iis_download(request,domain):
    """
    let's Encrypt下载iis证书包
    :param request:
    :param domain:
    :return:
    """
    if request.method == 'GET':
        filename = 'iis-'+domain+'.zip'
        file_abspath = '/root/.acme.sh/'+domain +'/' + filename
        if os.path.exists(file_abspath):
            file_download = open(file_abspath,'rb')
            response = FileResponse(file_download)
            response['Content-Type'] = 'application/octet-stream'
            response['Content-Disposition'] = 'attachment;filename=%s'%filename
            return response
        else:
            return redirect("/cert/apply/")


# ---------------------------------------------TrustAsia证书管理---------------------------------------------------------

def cert_TrustAsia_apply(requests):
    """
    TrustAsia证书申请页面
    :param requests:
    :return:
    """
    if requests.method == "GET":
        return render(requests,"cert_TrustAsia_apply.html")

def cert_TrustAsia_apply_create_order(requests):
    """
    TrustAsia创建订单
    :param requests:
    :return:
    """
    if requests.method == "POST":
        domain = requests.POST.get("domain")
        algorithm = requests.POST.get("algorithm")
        TrustAsia_obj = TrustAsia()
        response = TrustAsia_obj.Create_order(domain,algorithm)
        # response = {'msg': {'order_id': 'Dehz1wHa19bc3', 'auth_info': [{'auth_key': 'test52.linlim.cn', 'auth_value': '201806140731241a08yxu60kcc1x4lip25fnvtkzos5xag85ch85pncy2jrv449p', 'auth_path': '_dnsauth.test52'}]}, 'code': 0}
        return HttpResponse(json.dumps(response))

def cert_TrustAsia_apply_Order_Authz(requests):
    """
    TrustAsia验证订单
    :param requests:
    :return:
    """
    if requests.method == "POST":
        order = requests.POST.get("order")
        domain = requests.POST.get("domain")
        TrustAsia_obj = TrustAsia()
        response = TrustAsia_obj.Order_Authz(domain,order)
        return HttpResponse(json.dumps(response))
    else:
        return redirect("/cert/TrustAsia_apply/")

def cert_TrustAsia_download_nginx(requests,domain):
    """
    TrustAsia下载nginx证书包
    :param requests:
    :param domain:
    :return:
    """
    if requests.method == "GET":
        TrustAsia_obj = TrustAsia()
        file_abspath = TrustAsia_obj.Cert_nginx_download(domain)
        print(domain)
        filename = os.path.basename(file_abspath)
        if os.path.exists(file_abspath):
            file_download = open(file_abspath, 'rb')
            response = FileResponse(file_download)
            response['Content-Type'] = 'application/octet-stream'
            response['Content-Disposition'] = 'attachment;filename=%s' % filename
            return response
    else:
        return redirect("/cert/TrustAsia_order_list/")


def cert_TrustAsia_download_iis(requests,domain):
    """
    TrustAsia下载iis证书包
    :param requests:
    :param domain:
    :return:
    """
    if requests.method == "GET":
        TrustAsia_obj = TrustAsia()
        file_abspath = TrustAsia_obj.Cert_iis_download(domain)
        filename = os.path.basename(file_abspath)
        if os.path.exists(file_abspath):
            file_download = open(file_abspath, 'rb')
            response = FileResponse(file_download)
            response['Content-Type'] = 'application/octet-stream'
            response['Content-Disposition'] = 'attachment;filename=%s' % filename
            return response
        else:
            return redirect("/cert/TrustAsia_order_list/")

def TrustAsia_order_list(requests,page=1):
    """
    TrustAsia订单列表
    :param requests:
    :param page:
    :return:
    """
    if requests.method == "GET":
        TrustAsia_obj = TrustAsia()
        orderList = TrustAsia_obj.Order_list()
        paginator = Paginator(orderList["msg"]["orders"],10)
        try:
            one_page = paginator.page(page)
        except PageNotAnInteger:
            one_page = paginator.page(1)
        except EmptyPage:
            one_page = paginator.page(paginator.num_pages)

        if orderList.get("code") == 0:
            return render(requests,"TrustAsia_order_list.html",{"paginator":paginator,"one_page":one_page})
        else:
            return redirect("/cert/TrustAsia_apply/")

def TrustAsia_cert_list(requests,page=1):
    """
    TrustAsia证书列表
    :param requests:
    :return:
    """
    if requests.method == "GET":
        TrustAsia_obj = TrustAsia()
        certList = TrustAsia_obj.Cert_list()
        print(certList)
        paginator = Paginator(certList["msg"]["certs"],10)
        try:
            one_page = paginator.page(page)
        except PageNotAnInteger:
            one_page = paginator.page(1)
        except EmptyPage:
            one_page = paginator.page(paginator.num_pages)

        if certList.get("code") == 0:
            return render(requests,"TrustAsia_cert_list.html",{"paginator":paginator,"one_page":one_page})
        else:
            return redirect("/cert/TrustAsia_apply/")

def TrustAsia_order_detail(requests):
    """
    TrustAsia订单详情
    :param requests:
    :param order_id:
    :return:
    """
    if requests.method == "POST":
        TrustAsia_obj = TrustAsia()
        order_id = requests.POST.get("order_id")
        orderDetail = TrustAsia_obj.Orders_detail(order_id)
        if orderDetail["code"] == 0:
            return HttpResponse(json.dumps(orderDetail["msg"]["auth_info"][0]))
        else:
            return redirect("/cert/TrustAsia_apply/")

def TrustAsia_order_delete(requests):
    """
    TrustAsia删除订单
    :param requests:
    :return:
    """
    if requests.method == "POST":
        TrustAsia_obj = TrustAsia()
        order_id = requests.POST.get("order_id")
        status = requests.POST.get("status")
        result = TrustAsia_obj.Order_delete(order_id,status)
        return HttpResponse(json.dumps(result))


def TrustAsia_cert_detail(requests):
    if requests.method == "POST":
        sha1 = requests.POST.get("sha1")
        print(sha1)
        TrustAsia_obj = TrustAsia()
        cert_detail = TrustAsia_obj.Cert_detail(sha1)
        print(cert_detail)
        return HttpResponse(json.dumps(cert_detail))

def TrustAsia_cert_delete(requests):
    if requests.method == "POST":
        sha1 = requests.POST.get("sha1")
        TrustAsia_obj = TrustAsia()
        result = TrustAsia_obj.Cert_delete(sha1)
        return HttpResponse(json.dumps(result))

def TrustAsia_cert_select(requests,order_id):
    if requests.method == "GET":
        TrustAsia_obj = TrustAsia()
        result = TrustAsia_obj.Cert_select(order_id)
        print(result)
        if result.get("code") == 0:
            paginator = Paginator(result["msg"]["certs"], 10)
            try:
                one_page = paginator.page(1)
            except PageNotAnInteger:
                one_page = paginator.page(1)
            except EmptyPage:
                one_page = paginator.page(paginator.num_pages)
            return render(requests,"TrustAsia_cert_list.html",{"paginator":paginator,"one_page":one_page})
        else:
            return redirect("/cert/TrustAsia_apply/")
