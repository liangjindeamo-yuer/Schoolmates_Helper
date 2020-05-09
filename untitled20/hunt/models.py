from django.db import models
from django.db import models
from django.contrib.auth.models import AbstractUser
import django.utils.timezone
import datetime


class User(models.Model):
    username = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=20)
    repassword = models.CharField(max_length=200000,null=True)
    tel = models.PositiveIntegerField(blank=True, null=True)
    email = models.EmailField(max_length=30, unique=True)
    # 重构成icon 4.28
    icon = models.ImageField(upload_to='photo/%Y/%m/%d/', null=True, blank=True, default='photo/2020/04/26/1.jpg')
    qq = models.CharField(max_length=20, blank=True, null=True)
    wechat = models.CharField(max_length=20, blank=True, null=True)
    other = models.CharField(max_length=20, blank=True, null=True)
    is_active = models.BooleanField(default=False)
    is_delete = models.BooleanField(default=False)
    # 信誉度（没想好怎么实现）
    # 其他地方有用到吗？没有就直接改成rank
    rank = models.PositiveIntegerField(default=5)


class TaskType(models.Model):
    type_id = models.IntegerField(default=1)
    typename = models.CharField(max_length=32)
    typesort = models.IntegerField(default=1)

    def __str__(self):
        return self.typename


class Contact(models.Model):
    type_id = models.IntegerField(default=0)
    typename = models.CharField(max_length=32)

    def __str__(self):
        return self.typename


class Task(models.Model):
    # zjt新增的(2020年4月27日晚上讨论之后，另外新增的)，记得告诉 ly
    reason = models.CharField(max_length=128, null=True)

    comment_for_hunter = models.CharField(max_length=512, null=True)
    comment_for_publisher = models.CharField(max_length=512, null=True)
    contact_type_publisher = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='contact_publisher',
                                               verbose_name='发布人联系方式', db_constraint=False, null=True, default=0)
    contact_type_hunter = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='contact_hunter',
                                            verbose_name='委托人联系方式', db_constraint=False, null=True)
    task_name = models.CharField(max_length=32)
    task_sketch = models.CharField(max_length=512, null=True, blank=True)
    task_file = models.FileField(upload_to='%Y/%m/%d/', null=True, blank=True)
    task_type = models.ForeignKey(TaskType, default=0, on_delete=models.SET_DEFAULT)
    ddltime = models.DateField(default='2021-09-03')

    task_reward = models.IntegerField(default=0)

    is_pickedup = models.BooleanField(default=False)
    # 发布者确认
    is_finished = models.BooleanField(default=False)

    publisher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='publisher', verbose_name='发布人',
                                  null=True, blank=True)

    hunter = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='hunter', verbose_name='委托人',
                               db_constraint=False, null=True)

    def removehunter(self):
        self.hunter = None


class Revoke_reason(models.Model):
    revoke_reason = models.CharField(max_length=512, null=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='revoked_tasks', db_constraint=False)


# swf 2020年5月1日 (告诉ly) 任务下方讨论功能
class Discuss(models.Model):
    discussant = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='discuss_user', verbose_name='评论方',
                                   db_constraint=False, blank=False, null=False)
    discuss = models.CharField(max_length=512, blank=False, null=False)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='discussed_task')
    discusstime = models.DateTimeField(auto_now_add=True)


class Response(models.Model):
    response = models.CharField(max_length=512, blank=False, null=False)
    discuss = models.ForeignKey(Discuss, on_delete=models.CASCADE, related_name='response_discuss', null=True,
                                db_constraint=False)
    respondent = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='response_user', verbose_name='回复方',
                                   db_constraint=False, blank=False, null=False)
    responsetime = models.DateTimeField(auto_now_add=True)
