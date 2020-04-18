from django.shortcuts import render
from django.shortcuts import HttpResponse
from App import models
from App.models import MissionInfo
from App.models import UserInfo
from django.shortcuts import redirect
from App.models import Comment


def register(request):
    missions = MissionInfo.objects.all()
    context = {
        "missions": missions

    }
    return render(request,'register.html',context=context )


def acp(request):

    user = UserInfo.objects.get(pk=1)
    missions = user.missioninfo_set.all()
    context = {
        "missions":missions
    }
    return render(request,'acp.html',context=context)


def finish(request):
    user = UserInfo.objects.get(pk=1)
    missions = user.missioninfo_set.all()
    context = {
        "missions": missions
    }
    return render(request, 'finish.html', context=context)


def un_acp(request):
    user = UserInfo.objects.get(pk=1)
    missions = user.missioninfo_set.all()
    context = {
        "missions": missions
    }
    return render(request, 'un_acp.html', context=context)


def release(request):
    return render(request, 'release.html')


def f_mission(request):

    id = request.GET.get("id")
    mission = MissionInfo.objects.get(pk = id)
    mission.finish = True
    mission.save()
    request.session['id'] = id

    return redirect("/comment/")


def comment(request):
    if request.method == 'GET':
        return render(request, 'comment.html')
    elif request.method == 'POST':
        comment = request.POST.get('comment')
        comments = Comment()
        comments.comment1=comment
        comments.m_mission_id = request.session['id']
        comments.save()
        return redirect('/release/')

def d_mission(request):

    id = request.GET.get("id")
    mission = MissionInfo.objects.get(pk = id)
    mission.acp = False
    mission.save()
    request.session['id']=id

    return redirect("/reason/")


def reason(request):

    if request.method == 'GET':
        return render(request, 'reason.html')
    elif request.method == 'POST':
        reason = request.POST.get('reason')
        id = request.session['id']
        mission = MissionInfo.objects.get(pk = id)
        mission.reason = reason
        mission.save()
        return redirect("/release/")


def d_unacpm(request):
    id = request.GET.get("id")
    mission = MissionInfo.objects.get(pk=id)
    mission.delete()

    return redirect("/release/")


def m_detail(request):
    id = request.GET.get("id")
    mission = MissionInfo.objects.get(pk=id)
    context={
        "mission":mission
    }
    return render(request,'m_detail.html',context=context)


def m_change(request):
    if request.method == 'GET':
        id = request.GET.get("id")
        request.session['id'] = id
        mission = MissionInfo.objects.get(pk=id)
        context={
            "mission":mission
        }
        return render(request,'m_change.html',context=context)
    elif request.method == 'POST':
        id = request.session['id']
        Data = request.POST.get('Data')
        m1 = request.POST.get('m1')
        l = request.POST.get('l')
        d = request.POST.get('d')
        g = request.POST.get('g')
        mission = MissionInfo.objects.get(pk=id)
        mission.m_data = Data
        mission.mission1 = m1
        mission.m_label = l
        mission.m_detail = d
        mission.m_money = g
        mission.save()
        return redirect("/un_acp/")



