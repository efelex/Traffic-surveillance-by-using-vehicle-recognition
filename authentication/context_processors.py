from django.shortcuts import get_object_or_404
from authentication.models import Profile
from car_plate.models import Police_request
from django.conf import settings

user = settings.AUTH_USER_MODEL


def extras(request):
    user = request.user
    if user.is_authenticated:
        police_req = Police_request.objects.filter(police=user).first()
        profile_police = get_object_or_404(Profile, user=user)
        user_small = user.name
        user_small = user_small.split(' ')
        user_small = user_small[0][:2].upper()
        # to address notification from police request
        police_req = police_req

    else:
        profile_police = None
        user_small = None
        police_req = None

    return {
        'profile': profile_police,
        'user': user,
        'user_small': user_small,
        'police_req': police_req

    }
