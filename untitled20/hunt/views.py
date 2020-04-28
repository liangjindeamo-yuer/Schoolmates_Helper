# Create your views here.
from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import check_password
from hunt.form import User1, Task1
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import UserChangeForm
from django.core.exceptions import ValidationError
from hunt.models import *
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# 任务发布
def taskup0(request):
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
        task1.task_file = request.FILES.get('task_file')
        user_id = request.session.get('user_id')
        task1.publisher_id = user_id
        task1.save()
        return HttpResponse('发布成功')


# 新版任务发布，以这个为准，之前的先不删了，对应的前端是task_form.html
def task_up(request):
    if request.method == 'GET':
        task1 = Task1()
        return render(request, 'task_form.html', locals())
    else:
        task1 = Task1(request.POST, request.FILES)
        if task1.is_valid():
            user_id = request.session.get('user_id')
            task1.save()
            task1.cleaned_data['publisher_id'] = user_id
            Task.objects.create(**task1.cleaned_data)
            return HttpResponse('发布成功')
        else:
            return render(request, 'Task_form.html', locals())


def taskcopy(request):
    taskid0 = request.session.get('task_id')
    task = Task.objects.filter(task_id=taskid0)
    task.publisher_id = request.session.get('user_id')
    task.save()


# 用户登录
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
                user1.is_active = True
                user1.save()  # 登录状态修改
                request.session['username'] = user1.username
                request.session['user_id'] = user1.id
                # swf:第二轮之后实现，显示登录成功后几秒自动跳转到任务广场，现在先:直接到任务广场APP的视图
                return HttpResponseRedirect(reverse('tasks_square:task_square'))
            else:
                print('密码错误')
                return HttpResponse('密码错误')
        print('用户名不存在')
        return HttpResponse('用户名不存在')


# 注册
def index(request):
    if request.method == 'GET':
        user1 = User1()
        return render(request, 'data_form.html', locals())
    else:
        user1 = User1(request.POST, request.FILES)
        if user1.is_valid():
            user1.save()
            return HttpResponse('注册成功')
        else:
            return render(request, 'data_form.html', locals())


# 个人信息显示与修改
def edit0(request):
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id)
    if request.method == "POST":
        # 注意：这里由于用户名邮箱设置不能重名,所以这里的方法是调用修改后先把他改成一个其他的东西，
        # 这样子如果不修改用户名邮箱，之前的用户名邮箱就会替代这个乱码，这样可能会导致一些问题但目前还没遇到，，
        user.username = '121ub#$deded2ubu'
        user.email = '1@10.code21213fvm'
        user_form = User1(request.POST, request.FILES)
        user.save()
        if user_form.is_valid():
            user_cd = user_form.cleaned_data
            user.email = user_cd['email']
            user.tel = user_cd['tel']
            user.username = user_cd['username']
            user.qq = user_cd['qq']
            user.wechat = user_cd['wechat']
            user.other = user_cd['other']
            user.icon = user_cd['photo']
            user.save()
            return HttpResponse('ye')
        else:
            ErrorDict = user_form.errors

            return HttpResponse(ErrorDict)
    else:

        user_form = User1(instance=user)

        return render(request, 'edit.html', {"user_form": user_form})
