from django.shortcuts import render,HttpResponse,redirect
from cert.acme import ACME_cll
import json,os
import time
from django.http import FileResponse
# Create your views here.
from genericFunc import check_login

@check_login
def cert_list(request):
    acme_obj = ACME_cll()
    cert_info_list = acme_obj.getcertdir()
    if cert_info_list is None:
        return render(request,'cert_list.html',{'cert_dir':''})
    cert_dir = []
    for row in cert_info_list:
        cert_time = row.split('  ')
        if cert_time[1] == '':
            cert_dir.append({'domain':cert_time[0],'valid_day':''})
            continue
        valid_day = int((int(cert_time[1]) + 90*3600*24 - time.time()) / (3600 * 24))
        cert_dir.append({'domain':cert_time[0],'valid_day':valid_day})
    return render(request,'cert_list.html',{
        'cert_dir':cert_dir
    })

@check_login
def cert_apply(request):
    return render(request,'cert_apply.html')


@check_login
def cert_apply_postdomain(request):
    if request.method == 'POST':
        domain = request.POST.get('domain')
        acme_obj = ACME_cll(domain)
        result = acme_obj.generTXT()
        return HttpResponse(json.dumps(result))


@check_login
def cert_apply_genercert(request):
    if request.method == 'POST':
        domain = request.POST.get('domain')
        acme_obj = ACME_cll(domain)
        result = acme_obj.generCert()
        print(result)
        return HttpResponse(json.dumps(result))

@check_login
def cert_download(request,domain,file):
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
    if request.method == 'POST':
        domain = request.POST.get('domain')
        acme_obj = ACME_cll(domain)
        files = acme_obj.getcertfile()
        return HttpResponse(json.dumps(files))

@check_login
def cert_delete(request):
    if request.method == 'POST':
        domain = request.POST.get('domain')
        acme_obj = ACME_cll(domain)
        resute = acme_obj.cert_delete()
        if resute:
            return HttpResponse('OK')
        else:
            return HttpResponse('ERROR')