from django.shortcuts import render

# Create your views here.
def areas(request):
    return render(request,'show_areas.html')