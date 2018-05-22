from django.shortcuts import render,redirect

# Create your views here.


def login(request):
    if request.method == "GET":
        return render(request,'login.html')
    if request.method == "POST":
        user = request.POST.get('user')
        password = request.POST.get('password')
        print(user,password)
        if user == 'root@qq.com' and password == 'root':
            request.session['user'] = user
            request.session['password'] = password
            return redirect('/index/')
        else:
            return render(request, 'login.html')