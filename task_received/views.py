from django.shortcuts import render
from task_received.models import *
from django.urls import reverse
from django.http import HttpResponseRedirect


# 进入“我接受的任务”按钮
def index(request):
    return render(request, 'task_received/index.html')


# 全部已接受任务
def all_task_received(request):
    user_id = request.session.get('user_id')
    task_types = TaskType.objects.all()
    # task_received_list = Task.objects.filter(hunter_id=user_id),这里还没有登录，先改成下面这种
    task_received_list = Task.objects.all()
    context = {
        'task_types': task_types,
        'task_received_list': task_received_list,
    }
    return render(request, 'task_received/all_task_received.html', context)


def task_revoke(request, task_id):
    user_id = request.session.get('user_id')
    target_task = Task.objects.get(pk=task_id)
    target_task.is_pickedup = False
    target_task.hunter = None
    return HttpResponseRedirect(reverse('task_received:reasons_revoke', args=[task_id]))


def reasons_revoke(request, task_id):
    user_id = request.session.get('user_id')
    task = Task.objects.get(pk=task_id)
    return render(request, 'task_received/reasons_revoke.html', context={'task_id': task_id, 'task': task})


def task_detail(request, task_id):
    user_id = request.session.get('user_id')
    task = Task.objects.get(pk=task_id)
    return render(request, 'task_received/task_detail.html', context={'task': task})


def task_finished(request, task_id):
    user_id = request.session.get('user_id')
    task = Task.objects.get(pk=task_id)
    task.is_finished = True
    return render(request, 'task_received/task_finished', context={'task': task})


def task_sometype(request, tasktype_id):
    user_id = request.session.get('user_id')
    tasktype = TaskType.objects.get(pk=tasktype_id)
    task_types = TaskType.objects.all()
    # = Task.objects.filter(hunter_id=user_id,),这里还没有登录，先改成下面这种
    tasklist_sometype = Task.objects.filter(task_type=tasktype)
    return render(request, 'task_received/tasks_sometype.html',
                  context={'tasklist_sometype': tasklist_sometype, 'task_types': task_types})

def task_sometype_finished(request, tasktype_id):
    user_id = request.session.get('user_id')
    tasktype = TaskType.objects.get(pk=tasktype_id)
    task_types = TaskType.objects.all()
    # = Task.objects.filter(hunter_id=user_id,),这里还没有登录，先改成下面这种
    tasklist_sometype_finished = Task.objects.filter(task_type=tasktype,is_finished=True)
    return render(request, 'task_received/task_sometype_finished.html',
                  context={'tasklist_sometype_finished': tasklist_sometype_finished, 'task_types': task_types})

def task_sometype_not_finished(request, tasktype_id):
    user_id = request.session.get('user_id')
    tasktype = TaskType.objects.get(pk=tasktype_id)
    task_types = TaskType.objects.all()
    # = Task.objects.filter(hunter_id=user_id,),这里还没有登录，先改成下面这种
    tasklist_sometype_not_finished = Task.objects.filter(task_type=tasktype,is_finished=False)
    return render(request, 'task_received/task_sometype_not_finished.html',
                  context={'tasklist_sometype_not_finished': tasklist_sometype_not_finished, 'task_types': task_types})

def received_tasks_finished(request):
    user_id = request.session.get('user_id')
    task_types = TaskType.objects.all()
    # task_received_list = Task.objects.filter(hunter_id=user_id),这里还没有登录，先改成下面这种
    taskslist_received_finished = Task.objects.filter(is_finished=True)
    context = {
        'task_types': task_types,
        'taskslist_received_finished': taskslist_received_finished,
    }
    return render(request, 'task_received/received_tasks_finished.html', context)

def received_tasks_not_finished(request):
    user_id = request.session.get('user_id')
    task_types = TaskType.objects.all()
    # task_received_list = Task.objects.filter(hunter_id=user_id),这里还没有登录，先改成下面这种
    taskslist_received_not_finished = Task.objects.filter(is_finished=False)
    context = {
        'task_types': task_types,
        'taskslist_received_not_finished': taskslist_received_not_finished,
    }
    return render(request, 'task_received/received_tasks_not_finished.html', context)
