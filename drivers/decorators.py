from django.http import HttpResponse
from django.shortcuts import redirect


def is_verify_number_none(view_func):
    def wrapper_func(request, *args, **kwargs):

        if request.session.get('number') is None:
            return redirect('drivers_home')
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func


def is_car_detail_none(view_func):
    def wrapper_func(request, *args, **kwargs):

        if request.session.get('car_detail') is None:
            return redirect('drivers_home')
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func
