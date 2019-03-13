from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext, gettext_lazy as _

from user.models import *

User = get_user_model()

@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ['stu_id', 'tag', 'wechat_nickname', 'username']
    list_filter = ['tag', 'is_superuser']

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (_('AI圈用户信息'), {'fields': ('stu_id', 'wechat_nickname', 'name', 'tag', 'memo')}),
    )

    class Meta:
        model = User
        # fields = ['username', 'password', 'is_superuser', 'stu_id', 'wechat_nickname', 'name', 'tag', 'memo']

@admin.register(UserCheckInRecord)
class UserCheckInRecordAdmin(admin.ModelAdmin):
    list_display = ['get_user_stu_id', 'get_user_username', 'add_datetime', 'score', 'url', 'file_path']

    def get_user_stu_id(self, obj):
        return obj.user.stu_id
    get_user_stu_id.short_description = 'stu_id'

    def get_user_username(self, obj):
        return obj.user.username
    get_user_username.short_description = 'wechat_username'
