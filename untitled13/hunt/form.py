from django import forms
from .models import User,Task
from django.contrib.auth.forms import UserChangeForm
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm

class Task1(forms.ModelForm):
    class Meta:
        model = Task
        fields = '__all__'
        # exclude用于禁止模型字段转换表单字段
        exclude = ['publisher','is_pickedup','hunter','is_finished']
        labels = {
            'task_name': '任务名',
            'task_file': '相关文件（选填）',
            'task_reward': '任务奖励（必填）',
            'task_sketch': '任务描述（必填）',
            'publisher': '发布者',
            'hunter': '接收者',


        }

        error_messages = {
            '__all__': {
                'invalid': '请检查格式'},
            'name': {'required': '请输入',
                     'invalid': '请检查格式'
                     }
        }


class User1(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'
        # exclude用于禁止模型字段转换表单字段
        exclude = ['star','is_active','is_delete']
        labels = {
            'username': '用户名',
            'tel': '手机号（选填）',
            'qq': 'QQ（选填）',
            'wechat': '微信（选填）',
            'email': '邮箱',
            'other': '其他信息（选填）',
            'password': '密码',
            'star': '信誉'

        }

        error_messages = {
            '__all__': {
                'invalid': '请检查格式'},
            'name': {'required': '请输入',
                     'invalid': '请检查格式'
                     }
        }
