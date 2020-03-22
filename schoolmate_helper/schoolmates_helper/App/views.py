from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse

from App.models import MainWheel, User
from App.views_constant import *


def home(request):
    main_wheels = MainWheel.objects.all()
    data = {
        'title': '首页',
        'main_wheels': main_wheels,
    }

    return render(request, 'main/home.html', context=data)


def alltask(request):
    return render(request, 'main/alltask.html')


def task(request):
    return render(request, 'main/task.html')


def mine(request):
    return render(request, 'main/mine.html')


def register(request):
    if request.method == 'GET':
        data = {
            'title': '注册',
        }
        return render(request, 'user/register.html', context=data)
    elif request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        icon = request.FILES.get('icon')
        user = User()
        user.username = username
        user.email = email
        user.password = password
        user.icon = icon

        user.save()

        return redirect(reverse('App:login'))


def login(request):
    if request.method == 'GET':
        data = {
            'title': '登录',
        }
        return render(request, 'user/login.html', context=data)
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        users = User.objects.filter(username=username)
        if users.exists():
            users =users.filter(password=password)
            if users.exists():
                user = users.first()
                request.session['user_id']= user.id
                return redirect(reverse('App:mine'))
            else:
                print('密码错误')
                return redirect('App:login')
        print('用户名不存在')
        return redirect(reverse('App:login'))


def checkuser(request):
    username = request.GET.get('username')
    users = User.objects.filter(username=username)
    data = {
        'status': HTTP_OK,
        'msg': 'username available'
    }
    if users.exists():
        data['status'] = HTTP_USER_EXISTS
        data['msg'] = 'username already exists'
    else:
        pass
    return JsonResponse(data=data)


def checkemail(request):
    email = request.GET.get('email')
    emails = User.objects.filter(email=email)
    data = {
        'status': HTTP_OK,
        'msg': 'email available'
    }
    if emails.exists():
        data['status'] = HTTP_EMAIL_EXISTS
        data['msg'] = 'email already exists'
    else:
        pass
    return JsonResponse(data=data)


def checklogin(request):
    username = request.GET.get('username')
    password = request.GET.get('password')
    users = User.objects.filter(username=username)
    data = {
        'status': HTTP_OK,
        'msg': 'user available'
    }
    if users.exists():
        users = users.filter(password=password)
        if users.exists():
            pass
        else:
            data['status'] = HTTP_WRONG_PASSWORD
            data['msg'] = 'wrong password'
    else:
        data['status'] = HTTP_USERNAME_NOT_EXISTS
        data['msg'] = 'username does not exist'
    print(data)
    return JsonResponse(data=data)
