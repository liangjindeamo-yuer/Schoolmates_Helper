# _*_ coding: utf-8 _*_
# 开发团队：软件工程第5组
# 开发人员：莨瑾
# 开发时间：2020/3/21 16:32
# 文件名称: views_helper.py
# 开发工具：PyCharm
from django.core.mail import send_mail
from django.template import loader

from App.models import User
from schoolmates_helper.settings import *


def send_email_activate(username,receive,u_token):
    subject = 'SchoolHelper_activation'
    message = '<h1>Hello<h1>'
    from_email = EMAIL_HOST_USER
    recipient_list = [receive,]
    data = {
         'username':  username,
         'activate_url': 'http://'+SERVER_HOST+':'+SERVER_PORT+'/App/activate/?u_token='+u_token
    }
    html_message =loader.get_template('user/activate.html').render(data)
    send_mail(subject=subject,message=message,html_message=html_message,from_email=from_email,recipient_list=recipient_list)



def is_activated(user_id):
    user = User.objects.get(pk=user_id)
    if user.is_active:
        return True
    else:
        return False