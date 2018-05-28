from django.shortcuts import render,HttpResponse
from cert.acme import ACME_cll
import json
# Create your views here.

def cert_list(request):
    return render(request,'cert_list.html')


def cert_apply(request):
    return render(request,'cert_apply.html')

def cert_apply_postdomain(request):
    if request.method == 'POST':
        domain = request.POST.get('domain')
        acme_obj = ACME_cll(domain)
        result = acme_obj.generTXT()
        return HttpResponse(json.dumps(result))