from django.db import models


# Create your models here.
class MainWheel(models.Model):
    img = models.CharField(max_length=255)
    name = models.CharField(max_length=64)
    trackid = models.IntegerField(default=1)

    class Meta:
        db_table = 'smh_wheel'


class User(models.Model):
    username = models.CharField(max_length=32, unique=True)
    password = models.CharField(max_length=256)
    email = models.CharField(max_length=64, unique=True)
    icon = models.ImageField(upload_to='icons/%Y/%m/%d/')
    is_active = models.BooleanField(default=False)
    is_delete = models.BooleanField(default=False)

    class Meta:
        db_table = 'smh_user'
class TaskType(models.Model):
    type_id = models.IntegerField(default=1)
    typename = models.CharField(max_length=32)
    typesort = models.IntegerField(default=1)
    class  Meta:
        db_table = 'smh_tasktype'


class Task(models.Model):
    task_name = models.CharField(max_length=32)
    task_sketch = models.CharField(max_length=512,null=True)
    task_file = models.FileField(upload_to='task_file/%Y/%m/%d/',null=True)
    task_type = models.ForeignKey(TaskType,default=5,on_delete=models.SET_DEFAULT)

    task_date_year = models.IntegerField(default=2020,null=True)
    task_date_month = models.IntegerField(default=0,null=True)
    task_date_day = models.IntegerField(default=0,null=True)

    task_reward = models.IntegerField(default=0,null=True)

    is_pickedup = models.BooleanField(default=False)
    is_finished = models.BooleanField(default=False)

    publisher = models.ForeignKey(User,on_delete=models.CASCADE,related_name='publisher',verbose_name='发布人')
    hunter = models.ForeignKey(User,on_delete=models.DO_NOTHING,related_name='hunter',verbose_name='委托人',db_constraint=False,null=True)

    def removehunter(self):
        self.hunter = None
    class Meta:
        db_table = 'smh_task'


