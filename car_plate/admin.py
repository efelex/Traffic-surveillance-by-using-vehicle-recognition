from django.contrib import admin
from car_plate.models import Car_registration, Insurance, Car_Control, Tax, Captured, Charged_car, Charged_car_official, Dummy, Unregistered_car, Police_request

# Register your models here.
admin.site.register(Car_registration)
admin.site.register(Insurance)
admin.site.register(Car_Control)
admin.site.register(Tax)
admin.site.register(Captured)
admin.site.register(Charged_car)
admin.site.register(Charged_car_official)
admin.site.register(Dummy)
admin.site.register(Unregistered_car)
admin.site.register(Police_request)

