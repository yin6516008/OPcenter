from django.shortcuts import render,HttpResponse,redirect
from cert.acme import ACME_cll
import json,os
from django.http import FileResponse
# Create your views here.



def cert_list(request):
    acme_obj = ACME_cll()
    cert_dir = acme_obj.getcertdir()
    return render(request,'cert_list.html',{
        'cert_dir':cert_dir
    })


def cert_apply(request):
    return render(request,'cert_apply.html')

def cert_apply_postdomain(request):
    if request.method == 'POST':
        domain = request.POST.get('domain')
        acme_obj = ACME_cll(domain)
        result = acme_obj.generTXT()
        return HttpResponse(json.dumps(result))


def cert_apply_genercert(request):
    if request.method == 'POST':
        domain = request.POST.get('domain')
        acme_obj = ACME_cll(domain)
        result = acme_obj.generCert()
        if result == True:
            files = acme_obj.getcertfile()
            return HttpResponse(json.dumps({
              'status':'OK',
              'files':files
            }))
        else:
            return HttpResponse(json.dumps({
              'status':'ERROR',
              'data':result
            }))

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

def cert_getfile(request):
    if request.method == 'POST':
        domain = request.POST.get('domain')
        acme_obj = ACME_cll(domain)
        files = acme_obj.getcertfile()
        return HttpResponse(json.dumps(files))