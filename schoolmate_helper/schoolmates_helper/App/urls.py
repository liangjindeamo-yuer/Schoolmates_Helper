# _*_ coding: utf-8 _*_
# 开发团队：软件工程第5组
# 开发人员：莨瑾
# 开发时间：2020/3/20 16:15
# 文件名称: urls.py
# 开发工具：PyCharm
from django.urls import path

from App import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('alltask/', views.alltask, name='alltask'),
    path('task/', views.task, name='task'),
    path('mine/', views.mine, name='mine'),

    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('checkuser/', views.checkuser, name='checkuser'),
    path('checkemail/', views.checkemail, name='checkemail'),
    path('checklogin/', views.checklogin, name='checklogin'),
]
