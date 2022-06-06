from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.sites.shortcuts import get_current_site
from drivers.forms import LoginDriverForm, VerifyPinForm, CarAssignForm
from car_plate.models import Car_registration, Charged_car_official, Captured, Insurance, Tax, Car_Control
from codes.code_request import request_pin
from django.contrib import messages
from django.utils import timezone
from drivers.decorators import is_verify_number_none, is_car_detail_none
from drivers.process_payment import process_payment
from drivers.models import Payment_completed

now = timezone.now()
from django.db.models import Q


# Create your views here.

def home(request):
    return render(request, 'drivers/home.html')


def login_driver(request):
    form = LoginDriverForm()
    if request.method == 'POST':
        form = LoginDriverForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data.get('username')
            phone_number = Car_registration.objects.filter(owner_phone_number=phone_number).first()
            if phone_number:
                print("os ----------------------------", phone_number.id)
                code_number = request_pin()
                request.session['number'] = code_number
                return redirect('verify', id=phone_number.id)
            else:
                print("nopeee")

    return render(request, 'drivers/login.html', {'form': form})


@is_verify_number_none
def verify(request, id):
    number = request.session.get('number')
    form = VerifyPinForm()
    car_detail = get_object_or_404(Car_registration, id=id)
    print("number --------------", number)
    if request.method == 'POST':
        form = VerifyPinForm(request.POST)
        if form.is_valid():
            request.session['car_detail'] = id
            number_c = form.cleaned_data.get('number_code')
            print("number code ------------", number_c)
            if int(number) == number_c:
                del request.session['number']
                return redirect('driver_dashboard')
            else:
                messages.error(request, "Pin number not match")
    else:
        form = VerifyPinForm()
    return render(request, 'drivers/verify.html', {'form': form})


@is_car_detail_none
def driver_dashboard(request):
    car_detail = request.session.get('car_detail')
    car_detail = get_object_or_404(Car_registration, id=car_detail)
    phone_number = car_detail.owner_phone_number
    all_owner_car = Charged_car_official.objects.filter(
        Q(insurance_tole_expire__lt=now) | Q(control_tole_expire__lt=now) | Q(tax_tole_expire__lte=now) & Q(
            car__owner_phone_number=phone_number)).filter(car__owner_phone_number=phone_number)
    context = {
        'all_owner_car': all_owner_car,
        'now': now.date()
    }
    return render(request, 'drivers/driver_dashboard.html', context)


@is_car_detail_none
def driver_captured(request):
    car_detail = request.session.get('car_detail')
    car_detail = get_object_or_404(Car_registration, id=car_detail)
    phone_number = car_detail.owner_phone_number
    all_owner_car = Captured.objects.filter(car__owner_phone_number=phone_number)
    context = {
        'all_owner_car': all_owner_car
    }
    return render(request, 'drivers/driver_captured.html', context)


@is_car_detail_none
def driver_insurance(request):
    car_detail = request.session.get('car_detail')
    car_detail = get_object_or_404(Car_registration, id=car_detail)
    phone_number = car_detail.owner_phone_number
    all_owner_car = Insurance.objects.filter(car__owner_phone_number=phone_number)
    context = {
        'all_owner_car': all_owner_car
    }
    return render(request, 'drivers/driver_insurance.html', context)


@is_car_detail_none
def driver_tax(request):
    car_detail = request.session.get('car_detail')
    car_detail = get_object_or_404(Car_registration, id=car_detail)
    phone_number = car_detail.owner_phone_number
    all_owner_car = Tax.objects.filter(car__owner_phone_number=phone_number)
    context = {
        'all_owner_car': all_owner_car
    }
    return render(request, 'drivers/driver_tax.html', context)


@is_car_detail_none
def driver_control(request):
    car_detail = request.session.get('car_detail')
    car_detail = get_object_or_404(Car_registration, id=car_detail)
    phone_number = car_detail.owner_phone_number
    all_owner_car = Car_Control.objects.filter(car__owner_phone_number=phone_number)
    context = {
        'all_owner_car': all_owner_car
    }
    return render(request, 'drivers/driver_control.html', context)


@is_car_detail_none
def driver_payment(request, id):
    charged_car = get_object_or_404(Charged_car_official, id=id)
    context = {
        'charged_car': charged_car
    }
    return render(request, 'drivers/driver_payment.html', context)


@is_car_detail_none
def driver_assign_number(request):
    car_detail = request.session.get('car_detail')
    car_detail = get_object_or_404(Car_registration, id=car_detail)
    form = CarAssignForm(request.POST or None, instance=car_detail)
    if form.is_valid():
        form.save()
        return redirect('driver_assign_number')
    context = {
        'car_detail': car_detail,
        'form': form
    }
    return render(request, 'drivers/driver_assign_number.html', context)


# payment phase ======================== home
@is_car_detail_none
def payment_insurance(request, id):
    charged_car = get_object_or_404(Charged_car_official, id=id)
    phone_number = charged_car.car.owner_phone_number
    full_name = charged_car.car.owner_name
    charged_id = charged_car.id
    current_site = get_current_site(request=request).domain
    print("siteeeeeeeeeeeee", current_site)
    insurance_amount = charged_car.insurance_charged_amount

    return redirect(process_payment(phone_number, full_name, charged_id, insurance_amount, current_site))


@is_car_detail_none
def payment_insurance_completed(request, charged_id, amount):
    charged_car = get_object_or_404(Charged_car_official, id=charged_id)
    car = charged_car.car
    insurance_payment = amount
    Payment_completed.objects.create(car=car, insurance_payment=insurance_payment)
    Charged_car_official.objects.filter(id=charged_id).update(insurance_charged_amount=0, insurance_tole_expire=None)
    return redirect('driver_dashboard')


def logout_driver(request):
    del request.session['car_detail']
    return redirect('drivers_home')
