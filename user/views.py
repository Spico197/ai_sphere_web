import os
import datetime

import pandas as pd

from django.shortcuts import render, redirect
from ai_sphere.settings import ROLL_IN_DATA_DIR, CHECK_IN_DATA_DIR
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login, logout

from user.models import UserCheckInRecord

User = get_user_model()


def index(request):
    if request.method == 'POST':
        # print(request.POST)
        username = request.POST.get('wechat', '')
        password = request.POST.get('password', '')
        if username and password:
            user = authenticate(request, username=username, password=password)
            # print(user)
            if user is not None:
                login(request, user)
                # print('login')
                return redirect('user_panel')
            else:
                return render(request, 'index.html', {'instruction': "用户名或密码不对"})
        else:
            return render(request, 'index.html', {'instruction': "用户名或密码不能为空"})
    else:
        if request.user.is_authenticated:
            return redirect('user_panel')
    return render(request, 'index.html', {'instruction': "请登录"})

def panel(request):
    if request.user.is_authenticated:
        context = {
            'user': request.user,
        }
        if request.user.is_staff:
            return render(request, 'admin_user_panel.html', context=context)
        else:
            return render(request, 'common_user_panel.html', context=context)
    else:
        return redirect('user_index')

def user_logout(request):
    logout(request)
    return redirect('user_index')

def admin_load_in(request):
    if request.method == "POST":
        rollin_table = request.FILES.get('user_roll_in_table', None)
        if rollin_table:
            if rollin_table.name.split('.')[-1] not in ['xls', 'xlsx']:
                return render(request, 'admin_load_in.html', {'instruction': "请上传xls/xlsx格式的文件"})
            else:
                file_name = "rollin_table_{}.{}".format(datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'),
                                                       rollin_table.name.split('.')[-1])
                file_path_name = os.path.join(ROLL_IN_DATA_DIR, file_name)
                with open(file_path_name, 'wb') as f:
                    for chunk in rollin_table.chunks():
                        f.write(chunk)

                roll_in_data = pd.read_excel(file_path_name).to_dict()
                # print(roll_in_data)
                for stu_id, wechat_nickname, name, username in zip(roll_in_data['序号'].values(),
                                                                   roll_in_data['微信昵称'].values(),
                                                                   roll_in_data['姓名'].values(),
                                                                   roll_in_data['微信号'].values()):
                    print(stu_id, wechat_nickname, name, username)

                    user = User(username=username,
                                stu_id=stu_id, wechat_nickname=wechat_nickname, name=name,
                                is_staff=False, is_active=True)
                    user.set_password('123456')
                    user.save()

                return render(request, 'admin_load_in.html', {'instruction': "导入成功"})
        else:
            return render(request, 'admin_load_in.html', {'instruction': "请选择文件后再上传"})
    else:
        return render(request, 'admin_load_in.html')


def change_password(request):
    if request.user.is_authenticated:
        context = {
            'user': request.user,
            'instruction': '',
        }
        if request.method == 'POST':
            old_password = request.POST.get('old_password', '')
            new_password1 = request.POST.get('new_password1', '')
            new_password2 = request.POST.get('new_password2', '')
            if old_password and new_password1 and new_password2:
                if request.user.check_password(old_password):
                    if new_password1 == new_password2:
                        request.user.set_password(new_password1)
                        logout(request)
                        return redirect('user_index')
                    else:
                        context['instruction'] = '两次输入的新密码必须保持一致'
                else:
                    context['instruction'] = '旧密码输入错误'
            else:
                context['instruction'] = '请把三个密码框填满'

        return render(request, 'user_change_password.html', context=context)
    else:
        return redirect('user_index')

def under_construction(request):
    return render(request, 'under_construction.html')

def check_in(request):
    if request.user.is_authenticated:
        context = {
            'user': request.user,
        }
        context['activity_days'] = (datetime.datetime.now() - datetime.datetime(2019, 3, 9)).days + 1
        context['check_in_days'] = UserCheckInRecord.objects.filter(user=request.user).count()
        context['check_in_rate'] = context['check_in_days'] / context['activity_days']
        # print(context)
        check_in_rates = []
        for user in User.objects.all():
            check_in_rates.append(
                UserCheckInRecord.objects.filter(user=user).count() / context['activity_days']
            )
        # print(check_in_rates)
        check_in_rates = sorted(check_in_rates)
        check_in_rates.reverse()
        context['check_in_ranking'] = check_in_rates.index(context['check_in_rate']) + 1
        # print(context['check_in_ranking'])
        if request.method == "POST":
            # print(request.FILES)
            if UserCheckInRecord.objects.filter(user=request.user,
                                               add_datetime__year=datetime.datetime.now().year,
                                               add_datetime__month=datetime.datetime.now().month,
                                               add_datetime__day=datetime.datetime.now().day).count() != 0:
                context['instruction'] = '您今天已经打过卡'
                return render(request, 'user_check_in.html', context=context)

            score = request.POST.get('score', -1)
            share_url = request.POST.get('share_url', '')
            screen_paste_file = request.FILES.get('screen_paste', None)
            if score != -1 and screen_paste_file:
                if screen_paste_file.name.split('.')[-1] not in ['jpg', 'jpeg', 'png']:
                    context['instruction'] = '不支持的文件格式'
                    return render(request, 'user_check_in.html', context=context)
                file_path_name = os.path.join(CHECK_IN_DATA_DIR,
                                              '{}-{}-{}.{}'.format(request.user.stu_id,
                                                                  request.user.username,
                                                                  datetime.datetime.now().strftime('%Y-%m-%d'),
                                                                  screen_paste_file.name.split('.')[-1]))
                with open(file_path_name, 'wb') as f:
                    for chunk in screen_paste_file.chunks():
                        f.write(chunk)
                record = UserCheckInRecord(user=request.user, score=score, file_path=file_path_name)
                record.save()

                context['instruction'] = '打卡成功'
                return render(request, 'user_check_in.html', context=context)

            else:
                context['instruction'] = '成绩和成绩截图是必填项'
                return render(request, 'user_check_in.html', context=context)
        else:
            return render(request, 'user_check_in.html', context=context)
    else:
        return redirect('user_index')