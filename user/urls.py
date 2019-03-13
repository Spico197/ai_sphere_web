from django.urls import path

from user import views

urlpatterns = [
    path('index/', views.index, name='user_index'),
    path('panel/', views.panel, name='user_panel'),
    path('logout/', views.user_logout, name='user_logout'),
    path('change_password/', views.change_password, name='user_change_password'),
    path('check_in/', views.check_in, name='user_check_in'),
    path('mutual_evaluaiton/', views.under_construction, name='user_mutual_evaluaiton'),
    path('report_generation/', views.under_construction, name='user_report_generation'),
    path('certificate_download/', views.under_construction, name='user_certificate_download'),

    path('admin_load_in/', views.admin_load_in, name='user_load_in'),
    path('admin_mutual_evaluaiton_init/', views.under_construction, name='user_mutual_evaluaiton_init'),
    path('admin_report_generation_init/', views.under_construction, name='user_report_generation_init'),
    path('admin_certificate_download_init/', views.under_construction, name='user_certificate_download_init'),

]
