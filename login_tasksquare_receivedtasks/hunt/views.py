from django.shortcuts import render, redirect
from django.db.models import Q

from django.contrib.auth.hashers import check_password
from hunt.form import User1, Task1
from django.urls import reverse
from django.http import HttpResponse
from django.contrib.auth.forms import UserChangeForm
from django.core.exceptions import ValidationError
from hunt.models import *
# swf:加
from django.http import HttpResponseRedirect


# Create your views here.
def index(request):
    if request.method == 'GET':
        user1 = User1()
        return render(request, 'data_form.html', locals())
    else:
        user1 = User1(request.POST)
        if user1.is_valid():
            user1.save()
            return HttpResponse('注册成功')
        else:
            return render(request, 'data_form.html', locals())


def task_upload(request):
    if request.method == 'GET':
        user1 = Task1()
        return render(request, 'task_form.html', locals())
    else:
        user1 = Task1(request.POST)
        if user1.is_valid():
            user1.save()
            return HttpResponse('发布成功')
        else:
            return render(request, 'task_form.html', locals())


def login(request):
    if request.method == 'GET':
        data = {
            'title': '登录',
        }
        return render(request, 'login.html', context=data)
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        users = User.objects.filter(username=username)
        if users.exists():
            users = users.filter(password=password)
            if users.exists():
                user1 = users.first()
                # swf:这个active应该在邮箱验证以后变成True？
                user1.is_active = True
                # swf:第二轮之后实现，显示登录成功后几秒自动跳转到任务广场，现在先:直接到任务广场APP的视图
                # return HttpResponse('登陆成功')
                # 这样是添加username的缓存到session，然后其他的函数就可以用username = request.session.get('username')获取已经登录的用户名
                request.session['username'] = user1.username
                return HttpResponseRedirect(reverse('tasks_square:task_square'))
            else:
                print('密码错误')
                return HttpResponse('密码错误')
        print('用户名不存在')
        return HttpResponse('用户名不存在')
