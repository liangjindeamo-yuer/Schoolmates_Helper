# author：苏婉芳

from django.shortcuts import render
from task_received.models import *
from django.urls import reverse
from django.http import HttpResponseRedirect
# swf:删光models，加这个
from hunt.models import *


# 进入“我接受的任务”按钮
def index(request):
    return render(request, 'task_received/index.html')


def all_task_received(request):
    user_id = request.session.get('user_id')
    task_types = TaskType.objects.all()
    task_received_list = Task.objects.filter(hunter_id=user_id)
    context = {
        'task_types': task_types,
        'task_received_list': task_received_list,
    }
    return render(request, 'task_received/all_task_received.html', context)


def task_revoke(request, task_id):
    username = request.session.get('username')
    user = User.objects.get(username=username)
    target_task = Task.objects.get(pk=task_id)
    target_task.is_pickedup = False
    target_task.hunter = None
    target_task.save()
    return HttpResponseRedirect(reverse('task_received:all_task_received'))


def reasons_revoke(request, task_id):
    task = Task.objects.get(pk=task_id)
    request.session['task_id'] = task_id
    return render(request, 'task_received/reasons_revoke.html', context={'task_id': task_id, 'task': task})


# swf 2020年4月25日 新增
def revoke(request):
    reason = Revoke_reason()
    task = Task.objects.get(pk=request.session.get('task_id'))
    reason.task = task
    reason.revoke_reason = request.POST.get('reasons')
    task.is_pickedup = False
    task.hunter_id = None
    task.save()
    reason.save()
    return render(request, 'task_received/comment_or_revoke_successfuly.html',
                  context={'task': task, 'comment': 0, 'revoke': 1})


def task_detail(request, task_id):
    username = request.session.get('username')
    user = User.objects.get(username=username)
    task = Task.objects.get(pk=task_id)
    return render(request, 'task_received/task_detail.html', context={'task': task})


# swf：2020年4月25日 改动
def task_finished(request, task_id):
    task = Task.objects.get(pk=task_id)
    request.session['task_id'] = task_id
    return render(request, 'task_received/task_finished', context={'task': task})


# swf：2020年4月25日 新增
def comment(request):
    task = Task.objects.get(pk=request.session.get('task_id'))
    if request.method == 'GET':
        return render(request, 'task_received/task_finished', context={'task': task})
    else:
        username = request.session.get('username')
        user = User.objects.get(username=username)
        task.is_finished = True
        comment1 = Comment()
        comment1.task = task
        comment1.comment_for_publisher = request.POST.get('comment')
        comment1.save()
        task.save()
        return render(request, 'task_received/comment_or_revoke_successfuly.html',
                      context={'task': task, 'comment': 1, 'revoke': 0})


def task_sometype(request, tasktype_id):
    username = request.session.get('username')
    user_id = request.session.get('user_id')
    user = User.objects.get(username=username)
    tasktype = TaskType.objects.get(pk=tasktype_id)
    task_types = TaskType.objects.all()
    tasklist_sometype = Task.objects.filter(task_type=tasktype, hunter_id=user_id)
    return render(request, 'task_received/tasks_sometype.html',
                  context={
                      'tasklist_sometype': tasklist_sometype,
                      'task_types': task_types,
                      'typeid_now': tasktype_id
                  }
                  )


def task_sometype_finished(request, tasktype_id):
    username = request.session.get('username')
    user_id = request.session.get('user_id')
    user = User.objects.get(username=username)
    tasktype = TaskType.objects.get(pk=tasktype_id)
    task_types = TaskType.objects.all()
    tasklist_sometype_finished = Task.objects.filter(task_type=tasktype, is_finished=True, hunter_id=user_id)
    return render(request, 'task_received/task_sometype_finished.html',
                  context={'tasklist_sometype_finished': tasklist_sometype_finished,
                           'task_types': task_types,
                           'typeid_now': tasktype_id})


def task_sometype_not_finished(request, tasktype_id):
    user_id = request.session.get('user_id')
    username = request.session.get('username')
    user = User.objects.get(username=username)
    tasktype = TaskType.objects.get(pk=tasktype_id)
    task_types = TaskType.objects.all()
    # = Task.objects.filter(hunter_id=username,),这里还没有登录，先改成下面这种
    # tasklist_sometype_not_finished = Task.objects.filter(task_type=tasktype, is_finished=False)
    # swf:改 2020年4月17日
    tasklist_sometype_not_finished = Task.objects.filter(task_type=tasktype, is_finished=False, hunter_id=user_id)
    return render(request, 'task_received/task_sometype_not_finished.html',
                  context={'tasklist_sometype_not_finished': tasklist_sometype_not_finished,
                           'task_types': task_types,
                           'typeid_now': tasktype_id})


def received_tasks_finished(request):
    user_id = request.session.get('user_id')
    username = request.session.get('username')
    user = User.objects.get(username=username)
    task_types = TaskType.objects.all()
    taskslist_received_finished = Task.objects.filter(is_finished=True, hunter_id=user_id)
    context = {
        'task_types': task_types,
        'taskslist_received_finished': taskslist_received_finished,
    }
    return render(request, 'task_received/received_tasks_finished.html', context)


def received_tasks_not_finished(request):
    user_id = request.session.get('user_id')
    username = request.session.get('username')
    user = User.objects.get(username=username)
    task_types = TaskType.objects.all()
    taskslist_received_not_finished = Task.objects.filter(is_finished=False, hunter_id=user_id)
    context = {
        'task_types': task_types,
        'taskslist_received_not_finished': taskslist_received_not_finished,
    }
    return render(request, 'task_received/received_tasks_not_finished.html', context)
