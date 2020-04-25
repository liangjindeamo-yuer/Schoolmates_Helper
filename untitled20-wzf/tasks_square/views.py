# author：苏婉芳

from django.shortcuts import render
from hunt.models import *


def task_square(request):
    user_id = request.session.get('user_id')
    username = request.session.get('username')
    task_types = TaskType.objects.all()
    tasks_list = Task.objects.filter(is_pickedup=False).exclude(publisher_id=user_id)
    data = {
        'tasks_list': tasks_list,
        'task_types': task_types,
        'type_id': 0,
        'username': username,
    }
    return render(request, 'tasks_square/task_square.html', context=data)


def task_square_sort(request, type_id, order):
    user_id = request.session.get('user_id')
    username = request.session.get('username')
    task_types = TaskType.objects.all()

    if order == 'task_reward':
        ordername = '按酬劳升序'
    elif order == '-task_reward':
        ordername = '按酬劳降序'
    elif order =='ddltime':
        ordername = '按截止时间升序'
    elif order =='-ddltime':
        ordername = '按截止时间降序'
    else:
        ordername = '默认排序'

    if type_id != 0:
        sort = TaskType.objects.get(pk=type_id).typename
        tasks_list = Task.objects.filter(is_pickedup=False, task_type=type_id).order_by(order).exclude(
            publisher_id=user_id)
    else:
        sort = '全部任务'
        tasks_list = Task.objects.filter(is_pickedup=False).order_by(order).exclude(publisher_id=user_id)

    data = {
        'tasks_list': tasks_list,
        'username': username,
        'task_types': task_types,
        'type_id': type_id,
        'sort': sort,
        'ordername': ordername,
    }
    return render(request, 'tasks_square/task_square.html', context=data)


def check_hunt(request, task_id):
    task = Task.objects.get(pk=task_id)
    return render(request, 'tasks_square/check_hunt.html', context={'task': task})


def hunt_task(request, task_id):
    user_id = request.session.get('user_id')
    task = Task.objects.get(pk=task_id)
    task.is_pickedup = True
    task.hunter_id = user_id
    task.save()
    return render(request, 'tasks_square/hunt_successfully.html', context={'task': task})


def task_detail(request, task_id):
    task = Task.objects.get(pk=task_id)
    return render(request, 'tasks_square/task_detail.html', context={'task': task})
