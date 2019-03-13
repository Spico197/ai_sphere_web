from django.db import models
from django.contrib.auth.models import AbstractUser


class AIUser(AbstractUser):
    stu_id = models.IntegerField(default=-1, null=True)
    wechat_nickname = models.CharField(max_length=200, default='', null=True, blank=True)
    name = models.CharField(max_length=200, default='', null=True, blank=True)
    tag = models.CharField(max_length=20, choices=(
        ('0', '普通用户'), ('1', '名人堂'), ('2', '熟人圈')
    ), default='0', null=True)
    memo = models.TextField(default='', null=True, blank=True)

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name


class UserCheckInRecord(models.Model):
    user = models.ForeignKey(AIUser, on_delete=models.CASCADE)
    add_datetime = models.DateTimeField(auto_now_add=True)
    score = models.FloatField()
    url = models.URLField(null=True, blank=True)
    file_path = models.CharField(max_length=1000)

    class Meta:
        verbose_name = '用户打卡记录'
        verbose_name_plural = verbose_name


class UserScoreStat(models.Model):
    user = models.ForeignKey(AIUser, on_delete=models.CASCADE)
    url = models.URLField(null=True, blank=True)
    max_score = models.FloatField(null=True, blank=True)
    raise_number = models.IntegerField(null=True, blank=True)

    class Meta:
        verbose_name = '用户审计'
        verbose_name_plural = verbose_name
