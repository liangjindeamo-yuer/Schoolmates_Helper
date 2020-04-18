import uuid

from django.core.cache import cache
from django.core.mail import send_mail
from django.http import HttpResponse, JsonResponse, StreamingHttpResponse
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
    data = {
        'title': '发布任务',
    }
    if request.method == 'GET':
        return render(request, 'main/task.html', context=data)
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
        try:
            if taskreward:
               task.task_reward = float(eval(taskreward))
        except:
            pass
        task.task_file = taskfile
        user_id = request.session.get('user_id')
        task.publisher_id = user_id
        task.save()
        return render(request, 'main/task.html', context=data)


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
            'status':HTTP_OK,
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

        try:
            u_token = uuid.uuid4().hex
            cache.set(u_token, user.id, timeout=60 * 60 * 24)
            send_email_activate(username, email, u_token)
        except:
            data = {
                'title': '注册',
                'status':HTTP_WRONG_EMALL,
            }
            return render(request, 'user/register.html', context=data)
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
        user.rank += 1
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
        print(user.is_active)
        if is_login:
            if user.is_active:
                task.hunter_id = user_id
                task.is_pickedup = 1
                send_email_receive(task.publisher.username, user.username, task_id, task.task_name,
                                   task.publisher.email, user.email)
                task.save()
            else:
                data['status'] = HTTP_USER_NOT_ACTIVATE
        else:
            data['status'] = HTTP_USER_NOT_LOGIN
    except:
        data['status'] = HTTP_USER_NOT_LOGIN
    return JsonResponse(data=data)


def aboutus(request):
    user_id = request.session.get('user_id')
    data = {
        'title': '关于我们',
        'is_login': 0,
        'is_activate': 0,
    }
    if user_id:
        user = User.objects.get(pk=user_id)
        data['is_login'] = 1
        if user.is_active:
            data['is_activate'] = 1
    return render(request, 'mine_all/about us.html',data)


def callus(request):
    user_id = request.session.get('user_id')
    data = {
        'title': '关于我们',
        'is_login': 0,
        'is_activate': 0,
    }
    if user_id:
        user = User.objects.get(pk=user_id)
        data['is_login'] = 1
        if user.is_active:
            data['is_activate'] = 1
    return render(request, 'mine_all/callus.html',data)


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


def alltaskpublisher_sort(request, typeid, sort_way):
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
    send_email_relieve(task.publisher.username, task.hunter.username, task_id, task.task_name, task.hunter.email)
    task.is_pickedup = 0
    task.removehunter()
    task.save()
    data = {

    }
    return JsonResponse(data=data)


def relievetask2(request):
    task_id = request.GET.get('task_id')
    task = Task.objects.get(pk=task_id)
    send_email_relieve2(task.publisher.username, task.hunter.username, task_id, task.task_name, task.publisher.email)
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
        'title': "我的接受",
        'tasktypes': tasktypes,
        'task_list': task_list,
        'typeid': 0,
        'sort': '所有任务',
        'is_login': 1,
        'is_activate': 1,
    }
    return render(request, 'user/alltask_hunter.html', context=data)


def alltaskhunter_with_params(request, typeid):
    user_id = request.session.get('user_id')
    tasktypes = TaskType.objects.all()
    task_list = Task.objects.all().filter(task_type_id=typeid).filter(hunter_id=user_id)
    data = {
        'title': "我的接受",
        'tasktypes': tasktypes,
        'task_list': task_list,
        'typeid': typeid,
        'sort': '所有任务',
        'is_login': 1,
        'is_activate': 1,
    }
    return render(request, 'user/alltask_hunter.html', context=data)


def alltaskhunter_sort(request, typeid, sort_way):
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
        'title': "我的接受",
        'tasktypes': tasktypes,
        'task_list': task_list,
        'typeid': typeid,
        'sort': sort,
        'is_login': 1,
        'is_activate': 1,

    }
    return render(request, 'user/alltask_hunter.html', context=data)


def hunertask(request, typeid, sort_way):
    user_id = request.session.get('user_id')
    tasktypes = TaskType.objects.all()
    task_list = Task.objects.all().filter(hunter_id=user_id).filter(is_finished=0)
    if typeid == 0:
        pass
    else:
        task_list = task_list.filter(task_type_id=typeid)
    sort = '所有任务'
    if sort_way == 0:
        task_list = task_list.order_by('task_reward')
        sort = '酬劳'
    elif sort_way == 1:
        task_list = task_list.order_by('task_date_year', 'task_date_month', 'task_date_day')
        sort = '截止时间'
    elif sort_way == 4:
        pass
    data = {
        'title': "我的接受",
        'tasktypes': tasktypes,
        'task_list': task_list,
        'typeid': typeid,
        'sort': sort,
        'is_login': 1,
        'is_activate': 1,
    }
    return render(request, 'user/huntertask.html', context=data)


def publishertask(request, typeid, sort_way):
    user_id = request.session.get('user_id')
    tasktypes = TaskType.objects.all()
    task_list = Task.objects.all().filter(publisher_id=user_id).filter(is_pickedup=True).filter(is_finished=False)
    if typeid == 0:
        pass
    else:
        task_list = task_list.filter(task_type_id=typeid)
    sort = '所有任务'
    if sort_way == 0:
        task_list = task_list.order_by('task_reward')
        sort = '酬劳'
    elif sort_way == 1:
        task_list = task_list.order_by('task_date_year', 'task_date_month', 'task_date_day')
        sort = '截止日期'
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
    return render(request, 'user/publishertask.html', context=data)


def finishtask(request):
    task_id = request.GET.get('task_id')
    task = Task.objects.get(pk=task_id)
    task.is_finished = 1
    task.save()
    task.hunter.rank += 1
    task.hunter.save()
    send_email_finish(task.publisher.username, task.hunter.username, task_id, task.task_name, task.hunter.email)
    data = {

    }
    return JsonResponse(data=data)


def taskfinished(request, typeid, sort_way):
    user_id = request.session.get('user_id')
    tasktypes = TaskType.objects.all()
    task_list = Task.objects.all().filter(publisher_id=user_id) | Task.objects.all().filter(hunter_id=user_id)
    task_list = task_list.filter(is_finished=1)
    if typeid == 0:
        pass
    else:
        task_list = task_list.filter(task_type_id=typeid)
    sort = '所有任务'
    if sort_way == 0:
        task_list = task_list.filter(hunter_id=user_id)
        sort = '我接受的'
    elif sort_way == 1:
        task_list = task_list.filter(publisher_id=user_id)
        sort = '我发布的'
    elif sort_way == 4:
        pass
    data = {
        'title': "我的完成",
        'tasktypes': tasktypes,
        'task_list': task_list,
        'typeid': typeid,
        'sort': sort,
        'is_login': 1,
        'is_activate': 1,
    }
    return render(request, 'user/taskfinished.html', context=data)


def comment(request,typeid,sort_way):
    user_id = request.session.get('user_id')
    tasktypes = TaskType.objects.all()
    task_list = Task.objects.all()
    task_list = task_list.filter(is_finished=1).filter(publisher_id=user_id).filter(comment_publisher=None) | task_list.filter(is_finished=1).filter(hunter_id=user_id).filter(comment_hunter=None)
    if typeid == 0:
        pass
    else:
        task_list = task_list.filter(task_type_id=typeid)
    sort = '所有任务'
    if sort_way == 0:
        task_list = task_list.filter(hunter_id=user_id)
        sort = '我接受的'
    elif sort_way == 1:
        task_list = task_list.filter(publisher_id=user_id)
        sort = '我发布的'
    elif sort_way == 4:
        pass
    data = {
        'title': "待评价",
        'tasktypes': tasktypes,
        'task_list': task_list,
        'typeid': typeid,
        'sort': sort,
        'is_login': 1,
        'is_activate': 1,
    }

    return render(request,'user/taskcomment.html', context=data)

def taskcontent(request, task_id):
    task = Task.objects.get(pk=task_id)
    is_login = 0
    is_activate = 0
    data = {
        'task': task,
        'is_login': is_login,
        'is_activate': is_activate,
        'SERVER_HOST':SERVER_HOST,
        'SERVER_PORT':SERVER_PORT,
    }
    is_PorH = 0
    try:
        user_id = request.session.get('user_id')
        user = User.objects.get(pk=user_id)
        is_login = 1
        data['is_login'] = is_login
        data['user'] = user
        if user.is_active:
            is_activate = 1
            data['is_activate'] = is_activate
        if task.publisher.id == user_id:
            is_PorH = 1
        elif task.hunter.id  == user_id:
            is_PorH = 2
    except:
        pass
    if request.method == 'GET':
        return render(request, 'mine_all/taskcontent.html', context=data)
    elif request.method == 'POST':
        comment = request.POST.get('comment')
        if is_PorH == 1:
            task.comment_publisher = comment
            task.save()
        elif is_PorH == 2:
            task.comment_hunter = comment
            task.save()
        return render(request, 'mine_all/taskcontent.html', context=data)


def modifyuser(request):
    user_id = request.session.get('user_id')
    user = User.objects.get(pk=user_id)
    is_activate = 0
    if user.is_active:
        is_activate = 1
    if request.method == 'GET':
        data = {
            'title': '修改个人信息',
            'is_login': 1,
            'is_activate': is_activate,
            'user':user,
        }
        return render(request, 'user/modifyuser.html', context=data)
    elif request.method == 'POST':

        username = request.POST.get('username')
        if username:
            user.username = username
        email = request.POST.get('email')
        if email:
            user.email = email
            user.is_active = 0
        password = request.POST.get('password')
        if password:
            user.password = password
        try:
            icon = request.FILES.get('icon')
            if icon:
                user.icon = icon
        except:
            pass
        if user.rank !=0:
            user.rank -= 1
        user.save()

        u_token = uuid.uuid4().hex
        cache.set(u_token, user.id, timeout=60 * 60 * 24)
        send_email_activate(username, email, u_token)

        return redirect(reverse('App:mine'))


def modifytask(request,task_id):
    user_id = request.session.get('user_id')
    user = User.objects.get(pk=user_id)
    task = Task.objects.get(pk=task_id)
    data = {
        'title': '修改任务',
        'user' :  user   ,
        'task' :  task   ,
        'is_login':     1,
        'is_activate' : 1,
        'SERVER_HOST' : SERVER_HOST,
        'SERVER_PORT' : SERVER_PORT,
    }
    if request.method == 'GET':
        return render(request, 'user/modifytask.html', context=data)

    elif request.method == 'POST':
        taskname = request.POST.get('taskname')
        tasktype = request.POST.get('tasktype')
        tasksketch = request.POST.get('tasksketch')
        taskdate_year = request.POST.get('taskdate_year')
        taskdate_month = request.POST.get('taskdate_month')
        taskdate_day = request.POST.get('taskdate_day')
        taskreward = request.POST.get('taskreward')
        taskfile = request.FILES.get('taskfile')
        if taskname:
            task.task_name = taskname
        if tasksketch:
            task.task_sketch = tasksketch
        if tasktype:
            task.task_type_id = int(tasktype)
        now = datetime.datetime.now()
        delta = datetime.timedelta(days=1)
        deadline = now + delta
        try:
            if taskdate_year:
                task.task_date_year = int(eval(taskdate_year))
        except:
            pass
        try:
            if taskdate_month:
                task.task_date_month = int(eval(taskdate_month))
        except:
            pass
        try:
            if task.task_date_day:
                task.task_date_day = int(eval(taskdate_day))
        except:
            pass
        try:
            if taskreward:
                task.task_reward = float(eval(taskreward))
        except:
            pass
        if taskfile:
            task.task_file = taskfile
        task.save()
        href = '/App/taskcontent/'+str(task_id)
        return redirect(href)