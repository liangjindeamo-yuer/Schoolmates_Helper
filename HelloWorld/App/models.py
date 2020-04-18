from django.db import models


class UserInfo(models.Model):
    objects = models.Manager()
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=32)


class MissionInfo(models.Model):
    objects = models.Manager()
    mission1 = models.CharField(max_length=64)
    m_data = models.DateField()
    m_label = models.CharField(max_length=16)
    m_detail = models.CharField(max_length=128)
    acp = models.BooleanField()
    finish = models.BooleanField()
    reason = models.CharField(max_length=64)
    m_user = models.ForeignKey(UserInfo,  on_delete=None)
    m_money = models.FloatField()


class Comment(models.Model):
    objects = models.Manager()
    comment1 = models.CharField(max_length=128)
    m_mission = models.ForeignKey(MissionInfo, on_delete=None)