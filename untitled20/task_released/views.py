from django.shortcuts import render
from django.shortcuts import HttpResponse
from hunt import models
from hunt.models import Task
from hunt.models import User
from hunt.models import TaskType
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def acp(request):
    if request.method == 'GET':
        id2 = 0
        id1 = request.session['user_id']
        user = User.objects.get(pk=id1)
        missions = Task.objects.filter(publisher_id=user)
        context = {
            "missions": missions,
            "id2": id2
        }
        return render(request, 'task_released/acp.html', context=context)
    elif request.method == 'POST':
        if request.POST.get('task_type') == "0":
            id2 = 0
        elif request.POST.get('task_type') == "1":
            id2 = 1
        elif request.POST.get('task_type') == "2":
            id2 = 2
        elif request.POST.get('task_type') == "3":
            id2 = 3
        elif request.POST.get('task_type') == "4":
            id2 = 4
        elif request.POST.get('task_type') == "5":
            id2 = 5
        id1 = request.session['user_id']
        user = User.objects.get(pk=id1)
        missions = Task.objects.filter(publisher_id=user)
        context = {
            "missions": missions,
            "id2": id2,
        }
        return render(request, 'task_released/acp.html', context=context)


@csrf_exempt
def finish(request):
    if request.method == 'GET':
        id2 = 0
        id1 = request.session['user_id']
        user = User.objects.get(pk=id1)
        missions = Task.objects.filter(publisher_id=user)
        context = {
            "missions": missions,
            "id2": id2
        }
        return render(request, 'task_released/finish.html', context=context)
    elif request.method == 'POST':
        if request.POST.get('task_type') == "0":
            id2 = 0
        elif request.POST.get('task_type') == "1":
            id2 = 1
        elif request.POST.get('task_type') == "2":
            id2 = 2
        elif request.POST.get('task_type') == "3":
            id2 = 3
        elif request.POST.get('task_type') == "4":
            id2 = 4
        elif request.POST.get('task_type') == "5":
            id2 = 5
        id1 = request.session['user_id']
        user = User.objects.get(pk=id1)
        missions = Task.objects.filter(publisher_id=user)
        context = {
            "missions": missions,
            "id2": id2,
        }
        return render(request, 'task_released/finish.html', context=context)


@csrf_exempt
def un_acp(request):
    if request.method == 'GET':
        id2 = 0
        id1 = request.session['user_id']
        user = User.objects.get(pk=id1)
        missions = Task.objects.filter(publisher_id=user)
        context = {
            "missions": missions,
            "id2": id2
        }
        return render(request, 'task_released/un_acp.html', context=context)
    elif request.method == 'POST':
        if request.POST.get('task_type') == "0":
            id2 = 0
        elif request.POST.get('task_type') == "1":
            id2 = 1
        elif request.POST.get('task_type') == "2":
            id2 = 2
        elif request.POST.get('task_type') == "3":
            id2 = 3
        elif request.POST.get('task_type') == "4":
            id2 = 4
        elif request.POST.get('task_type') == "5":
            id2 = 5
        id1 = request.session['user_id']
        user = User.objects.get(pk=id1)
        missions = Task.objects.filter(publisher_id=user)
        context = {
            "missions": missions,
            "id2": id2,
        }
        return render(request, 'task_released/un_acp.html', context=context)


def f_mission(request):

    id1 = request.GET.get("id")
    mission = Task.objects.get(pk=id1)
    mission.is_finished = True
    mission.save()
    request.session['id'] = id1

    return redirect("/task_released/comment/")


@csrf_exempt
def comment(request):
    if request.method == 'GET':
        return render(request, 'task_released/comment.html')
    elif request.method == 'POST':
        comment1 = request.POST.get('comment')
        id1 = request.session.get("id")
        task = Task.objects.get(pk=id1)
        task.comment_for_hunter=comment1
        task.save()
        return redirect('/task_released/finish/')


def d_mission(request):

    id1 = request.GET.get("id")
    mission = Task.objects.get(pk=id1)
    mission.is_pickedup = False
    mission.save()
    request.session['id'] = id1

    return redirect("/task_released/reason/")

# 问题：应该就只能一个任务对应一个reason？大概要改一下。
@csrf_exempt
def reason(request):

    if request.method == 'GET':
        return render(request, 'task_released/reason.html')
    elif request.method == 'POST':
        reason = request.POST.get('reason')
        id1 = request.session['id']
        mission = Task.objects.get(pk=id1)
        mission.reason = reason
        mission.save()
        return redirect("/task_released/finish/")


def d_unacpm(request):
    id1 = request.GET.get("id")
    mission = Task.objects.get(pk=id1)
    mission.delete()

    return redirect("/task_released/finish/")


def m_detail(request):
    id1 = request.GET.get("id")
    mission = Task.objects.get(pk=id1)
    type = mission.task_type.typename
    context = {
        "mission": mission,
        "type": type
    }
    return render(request, 'task_released/m_detail.html', context=context)


@csrf_exempt
def m_change(request):
    if request.method == 'GET':
        id1 = request.GET.get("id")
        request.session['id'] = id1
        mission = Task.objects.get(pk=id1)
        type = mission.task_type.typename
        context = {
            "mission": mission,
            "type": type
        }
        return render(request, 'task_released/m_change.html', context=context)
    elif request.method == 'POST':
        id1 = request.session['id']
        Data = request.POST.get('Data')
        m1 = request.POST.get('m1')
        l = request.POST.get('task_type')
        d = request.POST.get('task_sketch')
        g = request.POST.get('g')
        file = request.POST.get('task_file')
        mission = Task.objects.get(pk=id1)
        type = TaskType.objects.get(pk=l)
        mission.ddltime = Data
        mission.task_name = m1
        mission.task_type = type
        mission.task_sketch = d
        mission.task_reward = g
        mission.task_file = file
        mission.save()
        return redirect("/task_released/un_acp/")


def download(request):
    site = request.GET.get('site')
    file = open(site,'rb')
    response = HttpResponse(file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment'
    return response
