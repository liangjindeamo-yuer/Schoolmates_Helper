from django.db import models
from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime

class User(models.Model):
    username = models.CharField(max_length=20,  unique=True)
    password = models.CharField(max_length=20, default='0')
    tel = models.PositiveIntegerField(blank=True, null=True)
    email = models.EmailField(max_length=30,unique=True)
    photo = models.ImageField(upload_to='static/%Y/%m/%d/',null=True,blank=True,default='static/1.jpg')
    qq = models.CharField(max_length=20, blank=True, null=True)
    wechat = models.CharField(max_length=20, blank=True, null=True)
    other = models.CharField(max_length=20, blank=True, null=True)
    #icon = models.ImageField(upload_to='icons/%Y/%m/%d/',blank=True, null=True)
    is_active = models.BooleanField(default=False)
    is_delete = models.BooleanField(default=False)
    # 信誉度（没想好怎么实现）
    star = models.PositiveIntegerField(default=5)

class TaskType(models.Model):
    type_id = models.IntegerField(default=1)
    typename = models.CharField(max_length=32)
    typesort = models.IntegerField(default=1)

class Task(models.Model):
    task_name = models.CharField(max_length=32)
    task_sketch = models.CharField(max_length=512, null=True, blank=True)
    task_file = models.FileField(upload_to='static/%Y/%m/%d/', null=True, blank=True)
    task_type = models.ForeignKey(TaskType,default=5,on_delete=models.SET_DEFAULT)
    ddltime=models.DateField(blank=True,null=True)

    task_reward = models.IntegerField(default=0, null=True, blank=True)

    is_pickedup = models.BooleanField(default=False)
    # 发布者确认
    is_finished = models.BooleanField(default=False)

    publisher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='publisher', verbose_name='发布人',
                                  null=True,blank=True)

    hunter = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='hunter', verbose_name='委托人',
                               db_constraint=False, null=True)

    def removehunter(self):
        self.hunter = None

# swf：以下全是2020年4月25日新增内容 未提交到github
# 今天写写评论、原因、原因展现在任务里面、评论展现在各自的个人信息、任务详情页可以点进去看发布方信息
class Comment(models.Model):
    comment_for_hunter = models.CharField(max_length=512,null=True)
    comment_for_publisher = models.CharField(max_length=512,null=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE,related_name='commented_tasks')

class  Revoke_reason(models.Model):
    revoke_reason = models.CharField(max_length=512,null=True)
    task = models.ForeignKey(Task,on_delete=models.CASCADE,related_name='revoked_tasks')
