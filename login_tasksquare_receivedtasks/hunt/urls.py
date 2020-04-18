from django.urls import path

from . import views

urlpatterns = [

    path('1/', views.index, name='index'),
    #注册,
    path('login/',views.login,name='login'),
    #登录
    path('up/',views.task_upload,name='up'),
    #任务发布
    ]