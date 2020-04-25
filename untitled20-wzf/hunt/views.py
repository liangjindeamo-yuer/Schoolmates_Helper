# Create your views here.
from django.shortcuts import render, redirect
from django.db.models import Q

from django.contrib.auth.hashers import check_password
from hunt.form import User1, Task1
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import UserChangeForm
from django.core.exceptions import ValidationError
from hunt.models import *
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


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


def task_up(request):
    if request.method == 'GET':
        task1 = Task()
        return render(request, 'task.html', locals())
    else:
        task1 = Task()
        task1.task_name = request.POST.get('task_name')
        task_type = request.POST.get('task_type')
        task1.task_reward = request.POST.get('task_reward')
        task1.task_sketch = request.POST.get('task_sketch')
        task1.task_type_id = int(task_type)
        task1.ddltime = request.POST.get('ddltime')
        task1.task_file = request.POST.get('task_file')
        user_id = request.session.get('user_id')
        task1.publisher_id = user_id
        task1.save()
        return render(request, 'task_up_successfully.html')


def login(request):
    if request.method == 'GET':
        data = {
            'title': '登录',
        }
        return render(request, 'login.html', context=data)
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        users = User.objects.filter(Q(username=username) | Q(email=username))
        if users.exists():
            users = users.filter(password=password)
            if users.exists():
                user1 = users.first()
                user1.is_active = True  # 登录状态修改
                request.session['username'] = user1.username
                request.session['user_id'] = user1.id
                # swf:第二轮之后实现，显示登录成功后几秒自动跳转到任务广场，现在先:直接到任务广场APP的视图
                return HttpResponseRedirect(reverse('tasks_square:task_square'))
            else:
                print('密码错误')
                return HttpResponse('密码错误')
        print('用户名不存在')
        return HttpResponse('用户名不存在')


def mine(request):
    data = {
        'title': '个人主页',
        'is_login': 0,
        'is_activate': 0,
    }
