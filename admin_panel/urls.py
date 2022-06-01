from django.urls import path
from admin_panel.views import *


urlpatterns = [
    path('', adminlogin, name='adminlogin'),
    path('adminhome/', admin_dashboard, name='admin_dashboard'),
    path('adminlogout/', adminlogout, name='adminlogout'),
    # section for approve , request and denie police request
    path('police_request/', police_request_list, name='police_request_list'),
    path('police_request_approve/<int:id>/', police_request_approve, name='police_request_approve'),
    path('police_request_denied/<int:id>/', police_request_denied, name='police_request_denied'),
    path('admin_all_captured/', admin_all_captured, name='admin_all_captured'),
    path('admin_unregistered_car/', admin_unregistered_car, name='admin_unregistered_car'),
    path('admin_urgence_car/', admin_urgence_car, name='admin_urgence_car'),
    # ============== all registered car ===========
    path('admin_registered_car/', admin_registered_car, name='admin_registered_car'),
    path('admin_insurance/', admin_insurance, name='admin_insurance'),
    path('admin_control/', admin_control, name='admin_control'),
    path('admin_tax/', admin_tax, name='admin_tax'),
    # email sent section and compose
    path('message/<int:id>/', admin_email_compose, name='admin_email_compose'),
    path('home_message/', home_message, name='home_message'),
    path('home_message_read/<int:id>/', home_message_read, name='home_message_read')
]