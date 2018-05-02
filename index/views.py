from django.shortcuts import render

# Create your views here.
def index(request):
    print('index')
    return render(request, 'index.html')

def show_areas(request):
    return render(request, 'areas.html')

