from django.db import models
from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime


class User(models.Model):
    username = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=20, default='0')
    tel = models.PositiveIntegerField(blank=True, null=True)
<<<<<<< HEAD
    email = models.EmailField(max_length=30,unique=True)
    photo = models.ImageField(upload_to='static/%Y/%m/%d/',null=True,blank=True,default='static/1.jpg')
=======
    email = models.EmailField(max_length=30, unique=True)
    # 重构成icon
    photo = models.ImageField(upload_to='photo/%Y/%m/%d/', null=True, blank=True, default='static/1.jpg')
>>>>>>> 3d9f7ec7a0d08b69e166ba83145d96e51a5bd8a7
    qq = models.CharField(max_length=20, blank=True, null=True)
    wechat = models.CharField(max_length=20, blank=True, null=True)
    other = models.CharField(max_length=20, blank=True, null=True)
    is_active = models.BooleanField(default=False)
    is_delete = models.BooleanField(default=False)
    # 信誉度（没想好怎么实现）
    # 其他地方有用到吗？没有就直接改成rank
    star = models.PositiveIntegerField(default=5)


class TaskType(models.Model):
    type_id = models.IntegerField(default=1)
    typename = models.CharField(max_length=32)
    typesort = models.IntegerField(default=1)

<<<<<<< HEAD

class Task(models.Model):
    task_name = models.CharField(max_length=32)
    task_sketch = models.CharField(max_length=512, null=True, blank=True)
    task_file = models.FileField(upload_to='static/%Y/%m/%d/', null=True, blank=True)
    task_type = models.ForeignKey(TaskType,default=5,on_delete=models.SET_DEFAULT)
    ddltime = models.DateField(blank=True,null=True)
    reason = models.CharField(max_length=128)
=======
# 不知道为什么 我打不开表 就没存几个typename
class Contact(models.Model):
    type_id = models.IntegerField(default=0)
    typename = models.CharField(max_length=32)

class Task(models.Model):
    # zjt新增的(2020年4月27日晚上讨论之后，另外新增的)，记得告诉 ly
    reason = models.CharField(max_length=128,null=True)

    comment_for_hunter = models.CharField(max_length=512, null=True)
    comment_for_publisher = models.CharField(max_length=512, null=True)
    contact_type_publisher = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='contact_publisher',
                                               verbose_name='发布人联系方式', db_constraint=False, null=True)
    contact_type_hunter = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='contact_hunter',
                                            verbose_name='委托人联系方式', db_constraint=False, null=True)
    task_name = models.CharField(max_length=32)
    task_sketch = models.CharField(max_length=512, null=True, blank=True)
    task_file = models.FileField(upload_to='%Y/%m/%d/', null=True, blank=True)
    task_type = models.ForeignKey(TaskType, default=5, on_delete=models.SET_DEFAULT)
    ddltime = models.DateField(blank=True, null=True)

>>>>>>> 3d9f7ec7a0d08b69e166ba83145d96e51a5bd8a7
    task_reward = models.IntegerField(default=0, null=True, blank=True)

    is_pickedup = models.BooleanField(default=False)
    # 发布者确认
    is_finished = models.BooleanField(default=False)

    publisher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='publisher', verbose_name='发布人',
                                  null=True, blank=True)

    hunter = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='hunter', verbose_name='委托人',
                               db_constraint=False, null=True)

    def removehunter(self):
        self.hunter = None


<<<<<<< HEAD
class Comments(models.Model):
    comment1 = models.CharField(max_length=128)
    m_mission = models.ForeignKey(Task, on_delete=None)


class Cnt(models.Model):
    cnt1 = models.CharField(max_length=128)
    c_mission = models.ForeignKey(Task, on_delete=None)
=======
class Revoke_reason(models.Model):
    revoke_reason = models.CharField(max_length=512, null=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='revoked_tasks')

>>>>>>> 3d9f7ec7a0d08b69e166ba83145d96e51a5bd8a7
