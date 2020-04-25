from django.urls import path

from . import views

urlpatterns = [

    path('1/', views.index, name='index'),
    #注册,
    path('login/',views.login,name='login'),
    #登录
    path('edit',views.edit0,name='edit'),
    #个人信息修改
    path('up0/',views.task_up,name='up0'),
    #任务发布
    ]