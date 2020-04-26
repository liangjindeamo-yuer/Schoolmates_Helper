from django.urls import path

from . import views

app_name = 'hunt'
urlpatterns = [

    path('1/', views.index, name='index'),
    #注册,
    path('login/',views.login,name='login'),
    #登录
    path('up0/',views.task_up,name='up0'),
    # 任务发布
    ]