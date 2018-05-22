from django.shortcuts import redirect


# ----------------------------------------验证是否登陆的装饰器-------------------------------------------------------------
# 登陆验证的装饰器
def check_login(func):
    def inner(request,*args,**kwargs):
        if  request.session.get('user',None) and request.session.get('password',None):
            return func(request, *args, **kwargs)
        return redirect("/login")
    return inner