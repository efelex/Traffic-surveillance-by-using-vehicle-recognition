from django.urls import path
from . import views
from django.contrib.auth import views as authViews
from car_plate.views import *


urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.signin, name='login'),
    # this will be toggled when 2fa is enabled
    path('verify_pin_login/', views.verify_pin_login, name='verify_pin_login'),
    path('signup/', views.signup, name='signup'),
    path('verify/', views.verify, name='verify'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', authViews.LogoutView.as_view(), {'next_page': 'login'}, name='logout'),

    # unverified police url
    path('verify_account/', views.unverified_police, name='unverified_police'),
    # request new pin
    path('new_pin/', views.request_new_pin, name='request_new_pin'),
    # request to be police traffic
    path('police_request_status/', views.police_request_status, name='police_request_status'),

    # detect car coming
    path('detect_car/', detect_car, name='detect_car'),
    path('automatic_detect_car/', automatic_detect_car, name='automatic_detect_car'),
    # danger warning
    path('danger/<int:id>/', views.warning_danger, name='warning_danger'),
    # profile management for traffic police
    path('police_profile/', views.police_profile, name='police_profile'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('update_main_profile/', views.update_main_profile, name='update_main_profile'),
    # password reset section
    path('reset_password/', views.reset_password, name='reset_password'),
    path('confirm_verify_pin/', views.confirm_verify_pin, name='confirm_verify_pin'),
    path('reset_confirm_password/', views.reset_confirm_password, name='reset_confirm_password'),
    path('reset_password_done/', views.reset_password_done, name='reset_password_done'),
    # enable two factor authentication
    path('enable_two_f/', views.enable_two_f, name='enable_two_f'),
    # activate or disable 2 factor
    path('enable_tf_functionality/', views.enable_tf_functionality, name='enable_tf_functionality'),

    # area of statistics and the data ==========================
    path('captured/', all_car_detection, name='all_car_detection'),
    path('urgence/', urgence_car, name='urgence_car'),
    path('charged_car_detected/', charged_car_detected, name='charged_car_detected'),

    # message from admin
    path('new_home_message/', new_home_message, name='new_home_message'),
    # home new message read
    path('new_home_message_read/<int:id>/', new_home_message_read, name='new_home_message_read'),















    # trial
    # path('verify/', verify, name='verify'),
    # path('register/', views.register, name='register'),
    # path('dashboard/', dashboard, name='dashboard'),
    # credential driver
]