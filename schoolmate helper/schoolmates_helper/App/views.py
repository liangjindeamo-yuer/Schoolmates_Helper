import uuid

from django.core.cache import cache
from django.core.mail import send_mail
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.template import loader
from django.urls import reverse

from App.models import *
from App.views_constant import *
from App.views_helper import *
from schoolmates_helper.settings import *
import datetime


def home(request):
    main_wheels = MainWheel.objects.all()
    data = {
        'title': '首页',
        'main_wheels': main_wheels,
        'is_login': 0,
        'is_activate': 0,
    }
    user_id = request.session.get('user_id')
    if user_id:
        user = User.objects.get(pk=user_id)
        data['user'] = user
        data['is_login'] = 1
        if user.is_active:
            data['is_activate'] = 1
        return render(request, 'user/home_alreadylogin.html', context=data)
    return render(request, 'main/home.html', context=data)


def alltask(request):
    user_id = request.session.get('user_id')
    tasktypes = TaskType.objects.all()
    task_list = Task.objects.all().filter(is_pickedup=0)
    data = {
        'title': "任务广场",
        'tasktypes': tasktypes,
        'task_list': task_list,
        'typeid': 0,
        'sort': '综合排序',
        'is_login': 0,
        'is_activate': 0,
    }
    if user_id:
        task_list = Task.objects.all().filter(is_pickedup=0).exclude(publisher_id=user_id).exclude(hunter_id=user_id)
        user = User.objects.get(pk=user_id)
        data['user'] = user
        data['is_login'] = 1
        data['task_list'] = task_list
        if user.is_active:
            data['is_activate'] = 1
    return render(request, 'main/alltask.html', context=data)


def alltask_with_params(request, typeid):
    user_id = request.session.get('user_id')
    tasktypes = TaskType.objects.all()
    task_list = Task.objects.all().filter(is_pickedup=0).filter(task_type_id=typeid)
    data = {
        'title': "任务广场",
        'tasktypes': tasktypes,
        'task_list': task_list,
        'typeid': typeid,
        'sort': '综合排序',
        'is_login': 0,
        'is_activate': 0,
    }
    if user_id:
        task_list = Task.objects.all().filter(is_pickedup=0).filter(task_type_id=typeid).exclude(
            publisher_id=user_id).exclude(hunter_id=user_id)
        user = User.objects.get(pk=user_id)
        data['user'] = user
        data['is_login'] = 1
        data['task_list'] = task_list
        if user.is_active:
            data['is_activate'] = 1
    return render(request, 'main/alltask.html', context=data)


def task(request):
    if request.method == 'GET':
        data = {
            'title': '发布任务',
        }
        return render(request, 'main/task.html')
    elif request.method == 'POST':
        task = Task()
        taskname = request.POST.get('taskname')
        tasktype = request.POST.get('tasktype')
        tasksketch = request.POST.get('tasksketch')
        taskdate_year = request.POST.get('taskdate_year')
        taskdate_month = request.POST.get('taskdate_month')
        taskdate_day = request.POST.get('taskdate_day')
        taskreward = request.POST.get('taskreward')
        taskfile = request.FILES.get('taskfile')
        task.task_name = taskname
        task.task_type_id = int(tasktype)
        task.task_sketch = tasksketch

        now = datetime.datetime.now()
        delta = datetime.timedelta(days=1)
        deadline = now + delta
        if taskdate_year:
            task.task_date_year = int(taskdate_year)
        else:
            task.task_date_year = deadline.year
        if taskdate_month:
            task.task_date_month = int(taskdate_month)
        else:
            task.task_date_month = deadline.month
        if task.task_date_day:
            task.task_date_day = int(taskdate_day)
        else:
            task.task_date_day = deadline.day

        task.task_reward = float(taskreward)
        task.task_file = taskfile
        user_id = request.session.get('user_id')
        task.publisher_id = user_id
        task.save()
        return render(request, 'main/task.html')


def mine(request):
    user_id = request.session.get('user_id')
    data = {
        'title': '个人主页',
        'is_login': 0,
        'is_activate': 0,
    }
    if user_id:
        user = User.objects.get(pk=user_id)
        data['is_login'] = 1
        data['user'] = user
        if user.is_active:
            data['is_activate'] = 1
        if user.icon:
            data['icon'] = MEDIA_KEY_PREFIX + user.icon.url
        if is_activated(user_id):
            return render(request, 'main/mine.html', context=data)
        else:
            return render(request, 'main/mine_not_activated.html', context=data)
    return render(request, 'main/mine_not_login.html', context=data)


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

        u_token = uuid.uuid4().hex
        cache.set(u_token, user.id, timeout=60 * 60 * 24)
        send_email_activate(username, email, u_token)

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
            users = users.filter(password=password)
            if users.exists():
                user = users.first()
                request.session['user_id'] = user.id
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


def alltask_sort(request, typeid, typesort1, typesort2, typesort3):
    tasktypes = TaskType.objects.all()
    print(typesort1)
    print(type(typesort1))
    if typeid != 0:
        task_list = Task.objects.all().filter(is_pickedup=0).filter(task_type_id=typeid).order_by(typesort1, typesort2,
                                                                                                  typesort3)
    else:
        task_list = Task.objects.all().filter(is_pickedup=0).order_by(typesort1, typesort2, typesort3)
    sort = '综合排序'
    if typesort1 == 'task_date_year':
        sort = '截止日期'
    elif typesort1 == 'task_reward':
        sort = '酬劳'
    data = {
        'title': "任务广场",
        'tasktypes': tasktypes,
        'task_list': task_list,
        'typeid': typeid,
        'sort': sort,
        'is_login': 0,
        'is_activate': 0,

    }
    try:
        user_id = request.session.get('user_id')
        user = User.objects.get(pk=user_id)
        if user_id:
            task_list = task_list.exclude(publisher_id=user_id).exclude(hunter_id=user_id)
            data['task_list'] = task_list
            data['is_login'] = 1
        if user.is_active:
            data['is_activate'] = 1
    except:
        pass
    return render(request, 'main/alltask.html', context=data)


def logout(request):
    request.session.flush()
    return redirect(reverse('App:mine'))


def activate(request):
    u_token = request.GET.get('u_token')
    user_id = cache.get(u_token)
    if user_id:
        user = User.objects.get(pk=user_id)
        user.is_active = True
        user.save()
        return HttpResponse('恭喜你，激活成功!')
    return HttpResponse('激活信息失效，请重新申请激活邮件')


def sendemail(request):
    try:
        user_id = request.session.get('user_id')
        user = User.objects.get(pk=user_id)
        u_token = uuid.uuid4().hex
        cache.set(u_token, user.id, timeout=60 * 60 * 24)

        send_email_activate(user.username, user.email, u_token)
        data = {
            'send_successfully': True,
        }
        return JsonResponse(data=data)
    except Exception as e:
        data = {
            'send_successfully': False,
        }
        return JsonResponse(data=data)


def receivetask(request):
    task_id = request.GET.get('task_id')
    task = Task.objects.get(pk=task_id)
    is_login = request.GET.get('is_login')
    data = {
        'status': HTTP_OK
    }
    try:
        user_id = request.session.get('user_id')
        user = User.objects.get(pk=user_id)
        print(is_login)
        if is_login:
            if user.is_active:
                task.hunter_id = user_id
                task.is_pickedup = 1
                task.save()
            else:
                data['status'] = HTTP_USER_NOT_ACTIVATE
        else:
            data['status'] = HTTP_USER_NOT_LOGIN
    except:
        data['status'] = HTTP_USER_NOT_LOGIN
    return JsonResponse(data=data)


def aboutus(request):
    return render(request, 'mine_all/about us.html')


def callus(request):
    return render(request, 'mine_all/callus.html')


def alltaskpublisher_with_params(request, typeid):
    user_id = request.session.get('user_id')
    tasktypes = TaskType.objects.all()
    task_list = Task.objects.all().filter(task_type_id=typeid).filter(publisher_id=user_id)
    data = {
        'title': "我的发布",
        'tasktypes': tasktypes,
        'task_list': task_list,
        'typeid': typeid,
        'sort': '所有任务',
        'is_login': 1,
        'is_activate': 1,
    }
    return render(request, 'user/alltask_publisher.html', context=data)


def alltaskpublisher_sort(request,typeid,sort_way):
    tasktypes = TaskType.objects.all()
    user_id = request.session.get('user_id')
    if typeid == 0:
        task_list = Task.objects.all().filter(publisher_id=user_id)
    else:
        task_list = Task.objects.all().filter(publisher_id=user_id).filter(task_type_id=typeid)
    sort = '所有任务'
    if sort_way == 0:
        task_list = task_list.filter(is_pickedup=0)
        sort = '未被接'
    elif sort_way == 1:
        task_list = task_list.filter(is_pickedup=1)
        sort = '已被接'
    elif sort_way == 4:
        pass
    data = {
        'title': "我的发布",
        'tasktypes': tasktypes,
        'task_list': task_list,
        'typeid': typeid,
        'sort': sort,
        'is_login': 1,
        'is_activate': 1,

    }
    return render(request, 'user/alltask_publisher.html', context=data)

def alltaskpublisher(request):
    user_id = request.session.get('user_id')
    tasktypes = TaskType.objects.all()
    task_list = Task.objects.all().filter(publisher_id=user_id)
    data = {
        'title': "我的发布",
        'tasktypes': tasktypes,
        'task_list': task_list,
        'typeid': 0,
        'sort': '所有任务',
        'is_login': 1,
        'is_activate': 1,
    }
    return render(request, 'user/alltask_publisher.html', context=data)


def relievetask(request):
    task_id = request.GET.get('task_id')
    task = Task.objects.get(pk=task_id)
    task.is_pickedup = 0
    task.removehunter()
    task.save()
    data = {

    }
    return JsonResponse(data=data)


def alltaskhunter(request):
    user_id = request.session.get('user_id')
    tasktypes = TaskType.objects.all()
    task_list = Task.objects.all().filter(hunter_id=user_id)
    data = {
        'title': "我的发布",
        'tasktypes': tasktypes,
        'task_list': task_list,
        'typeid': 0,
        'sort': '所有任务',
        'is_login': 1,
        'is_activate': 1,
    }
    return render(request, 'user/alltask_hunter.html', context=data)

def alltaskhunter_with_params(request,typeid):
    user_id = request.session.get('user_id')
    tasktypes = TaskType.objects.all()
    task_list = Task.objects.all().filter(task_type_id=typeid).filter(hunter_id=user_id)
    data = {
        'title': "我的发布",
        'tasktypes': tasktypes,
        'task_list': task_list,
        'typeid': typeid,
        'sort': '所有任务',
        'is_login': 1,
        'is_activate': 1,
    }
    return render(request, 'user/alltask_hunter.html', context=data)


def alltaskhunter_sort(request,typeid,sort_way):
    tasktypes = TaskType.objects.all()
    user_id = request.session.get('user_id')
    if typeid == 0:
        task_list = Task.objects.all().filter(hunter_id=user_id)
    else:
        task_list = Task.objects.all().filter(hunter_id=user_id).filter(task_type_id=typeid)
    sort = '所有任务'
    if sort_way == 0:
        task_list = task_list.filter(is_finished=0)
        sort = '未完成'
    elif sort_way == 1:
        task_list = task_list.filter(is_finished=1)
        sort = '已完成'
    elif sort_way == 4:
        pass
    data = {
        'title': "我的发布",
        'tasktypes': tasktypes,
        'task_list': task_list,
        'typeid': typeid,
        'sort': sort,
        'is_login': 1,
        'is_activate': 1,

    }
    return render(request, 'user/alltask_hunter.html', context=data)