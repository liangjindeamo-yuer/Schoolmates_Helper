# author：苏婉芳

from django.shortcuts import render
from hunt.models import *
from tasks_square.models import tasks_display_order


def task_square(request):
    all_tasks_not_picked = Task.objects.filter(is_pickedup=False)
    tasks_ordered_by_reward_down = all_tasks_not_picked.order_by('-task_reward')
    task_types = TaskType.objects.all()
    order = 'defalt'
    return render(request, 'tasks_square/task_square.html',
                  context={'all_tasks_not_picked': all_tasks_not_picked, 'task_types': task_types, 'order': order})


def check_hunt(request, task_id):
    task = Task.objects.get(pk=task_id)
    return render(request, 'tasks_square/check_hunt.html', context={'task': task})


def hunt_task(request, task_id):
    username = request.session.get('username')
    task = Task.objects.get(pk=task_id)
    task.is_pickedup = True
    task.hunter_id = username
    task.save()
    return render(request, 'tasks_square/hunt_successfully.html', context={'task': task})


def reward_up(request):
    task_types = TaskType.objects.all()
    all_tasks_not_picked = Task.objects.filter(is_pickedup=False)
    tasks_ordered_by_reward_up = all_tasks_not_picked.order_by('task_reward')
    order = 'reward_up'
    return render(request, 'tasks_square/task_square.html',
                  context={'order': order, 'tasks_ordered_by_reward_up': tasks_ordered_by_reward_up,
                           'task_types': task_types})


def reward_down(request):
    task_types = TaskType.objects.all()
    all_tasks_not_picked = Task.objects.filter(is_pickedup=False)
    tasks_ordered_by_reward_down = all_tasks_not_picked.order_by('-task_reward')
    order = 'reward_down'
    return render(request, 'tasks_square/task_square.html',
                  context={'order': order, 'tasks_ordered_by_reward_down': tasks_ordered_by_reward_down,
                           'task_types': task_types})

def task_detail(request, task_id):
    task = Task.objects.get(pk=task_id)
    return render(request, 'tasks_square/task_detail.html', context={'task': task})
