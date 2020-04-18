from django.db import models
from django.contrib.auth.models import AbstractUser


class User(models.Model):
    username = models.CharField(max_length=20, primary_key=True, unique=True)
    password = models.CharField(max_length=20, default='0')
    tel = models.PositiveIntegerField(blank=True, null=True)
    email = models.EmailField(max_length=30)
    qq = models.CharField(max_length=20, blank=True, null=True)
    wechat = models.CharField(max_length=20, blank=True, null=True)
    other = models.CharField(max_length=20, blank=True, null=True)
    #icon = models.ImageField(upload_to='icons/%Y/%m/%d/',blank=True, null=True)
    is_active = models.BooleanField(default=False)
    is_delete = models.BooleanField(default=False)
    # 信誉度（没想好怎么实现）
    star = models.PositiveIntegerField(default=5)

# swf:wyy的登录基础上加的
class TaskType(models.Model):
    type_id = models.IntegerField(default=1)
    typename = models.CharField(max_length=32)
    typesort = models.IntegerField(default=1)

class Task(models.Model):
    task_name = models.CharField(max_length=32)
    task_sketch = models.CharField(max_length=512, null=True, blank=True)
    task_file = models.FileField(upload_to='static/%Y/%m/%d/', null=True, blank=True)
    task_type = models.ForeignKey(TaskType,default=5,on_delete=models.SET_DEFAULT)
    # time=models.DateField()
    # 还是用这种显示时间？取决于在发布任务的时候怎么写的
    # task_date_year = models.IntegerField(default=2020, null=True)
    # task_date_month = models.IntegerField(default=0, null=True)
    # task_date_day = models.IntegerField(default=0, null=True)

    task_reward = models.IntegerField(default=0, null=True, blank=True)

    is_pickedup = models.BooleanField(default=False)
    # 发布者确认
    is_finished = models.BooleanField(default=False)

    publisher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='publisher', verbose_name='发布人')
    hunter = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='hunter', verbose_name='委托人',
                               db_constraint=False, null=True)

    def removehunter(self):
        self.hunter = None
# Create your models here.

