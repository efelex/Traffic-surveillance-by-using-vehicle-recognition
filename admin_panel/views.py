from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from car_plate.models import Unregistered_car, Dummy, Captured, Insurance, Tax, Car_Control, Charged_car_official, \
    Police_request, Car_registration
from django.db.models import Q
from django.utils import timezone
from django.contrib.auth import get_user_model
from authentication.utilis import send_sms_status
from admin_panel.forms import Admin_send_messageForm
from admin_panel.models import Send_message
from authentication.models import Profile

User = get_user_model()
now = timezone.now()


# Create your views here.

def admin_dashboard(request):
    user = request.user
    all_unregistered = Unregistered_car.objects.all().count()
    all_dummy = Dummy.objects.all().count()
    all_captured = Captured.objects.all().count()
    all_detected = all_captured + all_dummy + all_unregistered
    all_insurance = Insurance.objects.all().count()
    all_tax = Tax.objects.all().count()
    all_control = Car_Control.objects.all().count()
    all_end_varidation = Charged_car_official.objects.filter(
        Q(insurance_tole_expire__lt=now) | Q(control_tole_expire__lt=now) | Q(tax_tole_expire__lte=now)).count()
    user_all = User.objects.filter(is_verified_police=True).count()
    all_police_request = Police_request.objects.all().count()
    total_charged_car = Charged_car_official.objects.all().count()

    context = {
        'user': user,
        'captured': all_detected,
        'success': all_captured,
        'dummy': all_dummy,
        'unregistered': all_unregistered,
        'insurance': all_insurance,
        'tax': all_tax,
        'control': all_control,
        'urgence': all_end_varidation,
        'all_police': user_all,
        'all_request': all_police_request,
        'total_charged_car': total_charged_car

    }
    return render(request, 'super_temp/home.html', context)


def adminlogin(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        username = request.POST.get('phone_number')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_admin:

            login(request, user)
            return redirect('admin_dashboard')
        else:
            messages.error(request, "Admin only required or please check you credential")
    context = {
        'form': form
    }
    return render(request, 'super_temp/adminlogin.html', context)


def adminlogout(request):
    user = request.user
    login(request, user)
    return redirect('adminlogin')


def police_request_list(request):
    all_police_request = Police_request.objects.all()
    context = {
        'police_request': all_police_request
    }
    return render(request, 'super_temp/police_request.html', context)


def police_request_approve(request, id):
    police_req = get_object_or_404(Police_request, id=id)
    police_id = police_req.police.id
    if police_req.police.is_verified_police:
        return redirect('police_request_list')
    else:
        Police_request.objects.filter(id=id).update(police_status='approved')
        User.objects.filter(id=police_id).update(is_verified_police=True)
        status = 'Approved'
        phone_number = police_req.police.phone_number
        # send_sms_status(status, phone_number)
        return redirect('police_request_list')


def police_request_denied(request, id):
    police_request_denie = get_object_or_404(Police_request, id=id)
    Police_request.objects.filter(id=id).update(police_status='denied')
    police_id = police_request_denie.police.id
    User.objects.filter(id=police_id).update(is_verified_police=False)
    status = 'Denied'
    phone_number = police_request_denie.police.phone_number
    # send_sms_status(status, phone_number)
    return redirect('police_request_list')


# all =========== captured ==========

def admin_all_captured(request):
    all_car = Captured.objects.all().order_by('-time_done')
    context = {
        'car': all_car
    }
    return render(request, 'super_temp/admin_all_captured.html', context)


# unregistered_car

def admin_unregistered_car(request):
    unregistered = Unregistered_car.objects.all()
    context = {
        'car': unregistered
    }
    return render(request, 'super_temp/admin_unregistered_car.html', context)


def admin_urgence_car(request):
    all_end_varidation = Charged_car_official.objects.filter(
        Q(insurance_tole_expire__lt=now) | Q(control_tole_expire__lt=now) | Q(tax_tole_expire__lte=now))
    context = {
        'urgence': all_end_varidation,
        'now': now.date()
    }
    return render(request, 'super_temp/admin_urgence_car.html', context)


def admin_registered_car(request):
    all_car = Car_registration.objects.all()
    context = {
        'car': all_car
    }
    return render(request, 'super_temp/admin_registered_car.html', context)


def admin_insurance(request):
    now_date = now.date()
    all_insurance = Insurance.objects.all()
    context = {
        'insurance': all_insurance,
        'now_date': now_date
    }
    return render(request, 'super_temp/admin_insurance.html', context)


def admin_control(request):
    now_date = now.date()
    all_control = Car_Control.objects.all()
    context = {
        'control': all_control,
        'now_date': now_date
    }
    return render(request, 'super_temp/admin_control.html', context)


def admin_tax(request):
    now_date = now.date()
    all_tax = Tax.objects.all()
    context = {
        'tax': all_tax,
        'now_date': now_date
    }
    return render(request, 'super_temp/admin_tax.html', context)


# email section and send from admin ========================

def admin_email_compose(request, id):
    police_user = get_object_or_404(User, id=id)
    if request.method == 'POST':
        form = Admin_send_messageForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data.get('subject_message')
            body = form.cleaned_data.get('body_message')
            Send_message.objects.create(police_user=police_user, receiver_message=police_user.phone_number,
                                        subject_message=subject, body_message=body)
            messages.success(request, "message sent successfully")
            return redirect('admin_email_compose', id=police_user.id)
    else:
        form = Admin_send_messageForm()
    message_all_count = Send_message.objects.all().count()
    context = {
        'form': form,
        'police_user': police_user,
        'message_all_count': message_all_count
    }
    return render(request, 'super_temp/admin_email_compose.html', context)


def home_message(request):
    message_all = Send_message.objects.all()
    message_all_count = Send_message.objects.all().count()
    context = {
        'message_all': message_all,
        'message_all_count': message_all_count
    }
    return render(request, 'super_temp/home_message.html', context)


def home_message_read(request, id):
    message_info = get_object_or_404(Send_message, id=id)
    user_profile = get_object_or_404(Profile, user=message_info.police_user)
    message_all_count = Send_message.objects.all().count()
    context = {
        'message_info': message_info,
        'user_profile': user_profile,
        'message_all_count': message_all_count
    }
    return render(request, 'super_temp/home_message_read.html', context)
