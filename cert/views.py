from django.shortcuts import render

# Create your views here.

def cert_list(request):
    return render(request,'cert_list.html')


def cert_apply(request):
    return render(request,'cert_apply.html')