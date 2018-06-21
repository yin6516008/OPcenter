import hashlib
from django.shortcuts import render,redirect
from user.models import User

# Create your views here.

# 登录
def login(request):
    if request.method == "GET":
        return render(request,'login.html')
    if request.method == "POST":
        # 获取用户输入
        user = request.POST.get('user')
        password = request.POST.get('password')
        # 密码处理：先拼接，再MD5加密
        loginpw = user + '@' + password
        MD5 = hashlib.md5()
        MD5.update(loginpw.encode(encoding='utf-8'))
        md5_loginpw = MD5.hexdigest()

        # 获得数据库中该用户的密码等信息
        user_obj =  User.objects.filter(user_name=user).first()
        # 如果用户存在
        if user_obj is not None:
            # 密码验证通过
            if user_obj.password == md5_loginpw:
                # 保存session
                request.session['user'] = user
                request.session['password'] = md5_loginpw[-10]
                # 页面跳转
                return redirect('/index/')
            # 密码验证不通过
            else:
                return render(request, 'login.html', {'info': "Username or Password Error"})

        # 如果用户不存在
        else:
            return render(request, 'login.html', {'info': "Username or Password Error"})