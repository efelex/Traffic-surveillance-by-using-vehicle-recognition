from django.http import HttpResponse
from django.shortcuts import redirect


def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):

        if request.user.is_authenticated and not request.user.is_verified_police:
            return redirect('unverified_police')
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func


def is_a_police_user(view_func):
    def wrapper_func(request, *args, **kwargs):

        if request.user.is_authenticated and request.user.is_verified_police:
            return redirect('dashboard')
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func
