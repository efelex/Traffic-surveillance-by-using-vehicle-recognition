from django.urls import path
from drivers.views import *

urlpatterns = [
    path('', home, name='drivers_home'),
    path('login/', login_driver, name='login_driver'),
    path('verify/<str:id>/', verify, name='verify'),
    path('dashboard/', driver_dashboard, name='driver_dashboard'),
    path('captured/', driver_captured, name="driver_captured"),
    path('assign_number/', driver_assign_number, name="driver_assign_number"),
    path('insurance/', driver_insurance, name='driver_insurance'),
    path('tax/', driver_tax, name="driver_tax"),
    path('control/', driver_control, name="driver_control"),
    path('driver_payment/<int:id>/', driver_payment, name="driver_payment"),
    path('payment_insurance/<int:id>/', payment_insurance, name="payment_insurance"),
    path('payment_insurance_completed/<charged_id>/<amount>/', payment_insurance_completed, name="payment_insurance_completed"),
    path('logout_driver/', logout_driver, name='logout_driver')
]