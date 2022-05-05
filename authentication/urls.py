from django.urls import path
from . import views
from django.contrib.auth import views as authViews
from car_plate.views import *


urlpatterns = [
    path('', views.home, name='home'),
    path('login', views.signin, name='login'),
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
    path('danger/<int:id>/', views.warning_danger, name='warning_danger')

    # trial
    # path('verify/', verify, name='verify'),
    # path('register/', views.register, name='register'),
    # path('dashboard/', dashboard, name='dashboard'),
    # credential driver
]