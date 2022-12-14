from django.shortcuts import render, redirect, get_object_or_404
from authentication.models import Profile
from authentication.forms import UserForm
from codes.forms import CodeForm
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from car_plate.models import Captured, Dummy, Unregistered_car, Charged_car_official, Police_request
from django.utils import timezone
from authentication.decorators import unauthenticated_user, is_a_police_user
from authentication.utilis import send_sms, send_pin
from authentication.forms import NewPinForm, ResetPasswordForm, PasswordConfirmForm, UpdateMainForm, UpdateProfileForm
from codes.models import Code
from codes.code_request import request_pin
from authentication.models import Reset_password_request
from django.contrib.auth.decorators import login_required

now = timezone.now()

User = get_user_model()
from codes.models import Code


# Create your views here.

def home(request):
    return render(request, 'home/index.html')


def signin(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        username = request.POST.get('phone_number')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_verified and user.is_two_f_enable:
            request.session['pk'] = user.pk
            return redirect('verify_pin_login')
        if user is not None and not user.is_two_f_enable:
            if user.is_verified:
                login(request, user)
                return redirect('dashboard')
            elif user is not None and not user.is_verified:
                messages.info(request, 'please verify your account')
                return redirect('verify')


            else:
                messages.info(request, 'Username or password is incorrect')
        elif user is not None and not user.is_verified:
            messages.info(request, 'please verify your account')
            return redirect('verify')
        else:
            messages.info(request, 'Username or password is incorrect')
    context = {
        'form': form,
    }
    return render(request, 'dashboard/login.html', context)


# this will be applied when 2fa is enabled on
def verify_pin_login(request):
    form = CodeForm(request.POST or None)
    pk = request.session.get('pk')
    if pk:
        user = User.objects.get(pk=pk)
        code = user.code
        code_user = f"{user.name}: {user.code}"
        if not request.POST:
            print("code is ", code_user)

            # send code through intouch sms

            # send_sms(code_user, user.phone_number)
        if form.is_valid():
            num = form.cleaned_data.get('number')
            print("num -------------", num)
            print("code ----------------", code)
            if str(code) == num:
                code.save()
                login(request, user)
                del request.session['pk']
                return redirect('dashboard')
            elif str(code.number) == num:
                code.save()
                login(request, user)
                del request.session['pk']
                return redirect('dashboard')
            else:
                messages.error(request, "code pin not match")
    else:
        return redirect('login')

    return render(request, 'dashboard/verify_pin_login.html')


# end of 2fa accept functionality
def signup(request):
    form = UserForm()
    phone_number = request.POST.get('phone_number')
    user_check = User.objects.filter(phone_number=phone_number, is_verified=False)
    if user_check:
        user_check.delete()
        if request.method == 'POST':
            form = UserForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                phone_number = form.cleaned_data.get('phone_number')
                user = User.objects.get(phone_number=phone_number)
                print("user is", user)
                request.session['pk'] = user.pk
                return redirect('verify')
        else:
            form = UserForm()

    if not user_check:
        form = UserForm()
        if request.method == 'POST':
            form = UserForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                phone_number = form.cleaned_data.get('phone_number')
                user = User.objects.get(phone_number=phone_number)
                print("user is", user)
                request.session['pk'] = user.pk
                return redirect('verify')


        else:
            form = UserForm()
    context = {
        'form': form
    }
    return render(request, 'dashboard/signup.html', context)


def verify(request):
    form = CodeForm()
    pk = request.session.get('pk')
    if pk:
        user = User.objects.get(pk=pk)
        print("user-------------------------", user)
        phone_number = user.phone_number
        # code = Code.objects.g
        code = user.code
        code_user = f"{user.name}: {user.code}"
        if not request.POST:
            print("code is ", code_user)
            # send sms for verification
            # send_sms(code_user, user.phone_number)
        if request.method == 'POST':
            form = CodeForm(request.POST)
            if form.is_valid():
                num = form.cleaned_data.get('number')
                print("number code is --------------------", num)
                print("code to be checking --------------------", str(code))
                if str(code) == num:  # the reason why this line of code sometime it will not work is because in the model Code in app code we returned number and user for testing purpose but if we return number only ti will work for sure
                    code.save()
                    User.objects.filter(phone_number=phone_number).update(is_verified=True)
                    del request.session['pk']
                    return redirect('login')

                elif str(code.number) == num:
                    User.objects.filter(phone_number=phone_number).update(is_verified=True)
                    del request.session['pk']
                    return redirect('login')
                else:
                    messages.error(request, 'you verification code not match')
                    return redirect('verify')
    else:
        return redirect('login')
    return render(request, 'dashboard/verify.html', {'form': form})


@login_required(login_url='login')
@unauthenticated_user
def dashboard(request):
    user = request.user
    all_unregistered = Unregistered_car.objects.filter(police=user).count()
    all_dummy = Dummy.objects.filter(police=user).count()
    all_captured = Captured.objects.filter(police=user).count()
    all_detected = all_captured + all_dummy + all_unregistered

    context = {
        'user': user,
        'captured': all_detected,
        'success': all_captured,
        'dummy': all_dummy,
        'unregistered': all_unregistered,

    }
    return render(request, 'dashboard/home.html', context)


@login_required(login_url='login')
@unauthenticated_user
def warning_danger(request, id):
    charged_danger = get_object_or_404(Charged_car_official, id=id)
    car_description = charged_danger.car
    insurance_danger = charged_danger.insurance_tole_expire
    control_danger = charged_danger.control_tole_expire
    tax_danger = charged_danger.tax_tole_expire
    now_date = now.date()
    context = {
        'car': car_description,
        'insurance_danger': insurance_danger,
        'control_danger': control_danger,
        'tax_danger': tax_danger,
        'now_date': now_date
    }

    return render(request, 'dashboard/warning_danger.html', context)


@is_a_police_user
@login_required(login_url='login')
def unverified_police(request):
    police_user = request.user
    try:
        check_request = Police_request.objects.filter(police=police_user).first()
        check_request = check_request.police_status
    except:
        check_request = 'wait'
    context = {
        'check_request': check_request
    }
    return render(request, 'dashboard/unverified_police.html', context)


@login_required(login_url='login')
def police_request_status(request):
    police_user = request.user
    all_request = Police_request.objects.filter(police=police_user).first()
    if not all_request:
        Police_request.objects.create(police=police_user, police_status='pending')
        return redirect('unverified_police')
    if all_request:
        messages.info(request, 'please be patient you request is under review')
        return redirect('unverified_police')


def request_new_pin(request):
    form = NewPinForm()
    if request.method == 'POST':
        form = NewPinForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data.get('phone_number')
            phone_number = f'+{phone_number}'
            user_phone = User.objects.filter(phone_number=phone_number).first()
            if user_phone:
                if user_phone.is_verified:
                    print("verified --------------------")
                    # return redirect('verify')
                else:
                    print("not verified -------------------")
                    new_code = request_pin()
                    Code.objects.filter(user__phone_number=phone_number).update(number=new_code)
                    user_for_code = Code.objects.filter(user__phone_number=phone_number).first()
                    print("user ---code ----", user_for_code.number)
                    request.session['pk'] = user_for_code.pk
                    return redirect('verify')


            else:
                print("phone ----------number-----------false")
    return render(request, 'dashboard/request_pin.html')


@login_required(login_url='login')
def police_profile(request):
    user = request.user
    user_profile = get_object_or_404(Profile, user=user)
    user_num = 40
    if user_profile.user_image:
        user_image_n = 10
    else:
        user_image_n = 0
    if user_profile.date_of_birth:
        date_birth_n = 10
    else:
        date_birth_n = 0
    if user_profile.id_number:
        id_number_n = 10
    else:
        id_number_n = 0
    if user_profile.email:
        email_n = 10
    else:
        email_n = 0
    if user_profile.rank:
        rank_n = 10
    else:
        rank_n = 0
    if user_profile.residence:
        residence_n = 10
    else:
        residence_n = 0
    profile_complete = user_num + user_image_n + date_birth_n + id_number_n + email_n + rank_n + residence_n
    print(" -------------------------------- ", profile_complete)
    context = {
        'number_complete': profile_complete
    }

    return render(request, 'dashboard/police_profile.html', context)


@login_required(login_url='login')
def update_profile(request):
    user = request.user
    user_profile = get_object_or_404(Profile, user=user)
    form = UpdateProfileForm(request.POST or None, instance=user_profile)
    if request.method == 'POST':
        form = UpdateProfileForm(request.POST or None, request.FILES or None, instance=user_profile)
        if form.is_valid():
            form.save('update_profile')
    context = {
        'form': form
    }
    return render(request, 'dashboard/update_profile.html', context)


@login_required(login_url='login')
def update_main_profile(request):
    user = request.user
    phone_number = user.phone_number
    user_main = get_object_or_404(User, phone_number=phone_number)
    form = UpdateMainForm(request.POST or None, instance=user_main)
    if form.is_valid():
        form.save('update_main_profile')
    context = {
        'form': form
    }
    return render(request, 'dashboard/update_main_profile.html', context)


# password reset  ============================ section
def reset_password(request):
    form = ResetPasswordForm()
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data.get('phone_number')
            phone_number = f'+{phone_number}'
            user_phone = User.objects.filter(phone_number=phone_number).first()
            if user_phone:
                print("user registered --------------------")
                new_code = request_pin()
                user_request = Reset_password_request.objects.filter(user=user_phone).first()
                if user_request:
                    pass_reset = Reset_password_request.objects.filter(user=user_phone).update(pin=new_code)
                    pass_reset = Reset_password_request.objects.filter(user=user_phone).first()
                    # print("phone_number ----------yesss---------", new_code)
                    request.session['pk'] = pass_reset.pk
                    return redirect('confirm_verify_pin')
                else:
                    pass_reset = Reset_password_request.objects.create(user=user_phone, pin=new_code)
                    pass_reset = Reset_password_request.objects.filter(user=user_phone).first()
                    # print("phone_number ----hhh---------------", new_code)
                    request.session['pk'] = pass_reset.pk
                    return redirect('confirm_verify_pin')

                # return redirect('verify')
            else:
                print("user not registered -----------")
                return redirect('confirm_verify_pin')
    return render(request, 'dashboard/reset_password.html')


def confirm_verify_pin(request):
    form = CodeForm()
    pk = request.session.get('pk')
    if pk:
        police_who_request = Reset_password_request.objects.get(pk=pk)
        user_police = police_who_request.user
        code = police_who_request.pin
        code_user = f"{user_police.name}: {police_who_request.pin}"
        if not request.method == 'POST':
            print("code is ------------------- ", code_user)
            # send_pin(code_user, user_police.phone_number)
        if request.method == 'POST':
            form = CodeForm(request.POST)
            if form.is_valid():
                num = form.cleaned_data.get('number')
                if str(code) == num:
                    request.session['pk'] = user_police.pk
                    return redirect('reset_confirm_password')
                else:
                    messages.error(request, 'you verification code not match')
                    return redirect('confirm_verify_pin')
    return render(request, 'dashboard/confirm_verify_pin.html')


def reset_confirm_password(request):
    form = PasswordConfirmForm
    try:
        pk = request.session.get('pk')
        user = User.objects.get(pk=pk)
        if request.method == 'POST':
            form = PasswordConfirmForm(request.POST)
            if form.is_valid():
                password = form.cleaned_data.get('password')
                user.set_password(password)
                user.save()
                del request.session['pk']
                return redirect('reset_password_done')
            else:
                messages.error(request, 'password not match')

        else:
            form = PasswordConfirmForm
    except:
        return redirect('login')
    return render(request, 'dashboard/reset_confirm_password.html')


def reset_password_done(request):
    return render(request, 'dashboard/reset_password_done.html')


# enable two-factor authentication

@login_required(login_url='login')
@unauthenticated_user
def enable_two_f(request):
    return render(request, 'dashboard/enable_two_f.html')


@login_required(login_url='login')
@unauthenticated_user
def enable_tf_functionality(request):
    user = request.user
    phone_number = user.phone_number
    if user.is_two_f_enable:
        User.objects.filter(phone_number=phone_number).update(is_two_f_enable=False)
        messages.success(request, "2FA disabled successful")
        return redirect('enable_two_f')
    if not user.is_two_f_enable:
        User.objects.filter(phone_number=phone_number).update(is_two_f_enable=True)
        messages.success(request, '2FA enabled successful')
        return redirect('enable_two_f')

# def register(request):
#     form = UserForm()
#     phone_number = request.POST.get('phone_number')
#     user_check = User.objects.filter(phone_number=phone_number, is_verified=False)
#     if user_check:
#         user_check.delete()
#         if request.method == 'POST':
#             form = UserForm(request.POST, request.FILES)
#             if form.is_valid():
#                 form.save()
#                 phone_number = form.cleaned_data.get('phone_number')
#                 user = User.objects.get(phone_number=phone_number)
#                 print("user is", user)
#                 request.session['pk'] = user.pk
#                 return redirect('verify')
#         else:
#             form = UserForm()
#
#     if not user_check:
#         if request.method == 'POST':
#             form = UserForm(request.POST, request.FILES)
#             if form.is_valid():
#                 form.save()
#                 phone_number = form.cleaned_data.get('phone_number')
#                 user = User.objects.get(phone_number=phone_number)
#                 print("user is", user)
#                 request.session['pk'] = user.pk
#                 return redirect('verify')
#
#
#         else:
#             form = UserForm()
#     context = {
#         'form': form
#     }
#     return render(request, 'register.html', context)


# def verify(request):
#     form = CodeForm()
#     pk = request.session.get('pk')
#     if pk:
#         user = User.objects.get(pk=pk)
#         phone_number = user.phone_number
#         # code = Code.objects.g
#         code = user.code
#         code_user = f"{user.name}: {user.code}"
#         if not request.POST:
#             print("code is ", code_user)
#         if request.method == 'POST':
#             form = CodeForm(request.POST)
#             if form.is_valid():
#                 num = form.cleaned_data.get('number')
#                 print("number code is", num)
#                 if str(code) == num:
#                     code.save()
#                     User.objects.filter(phone_number=phone_number).update(is_verified=True)
#                     return redirect('dashboard')
#                 else:
#                     messages.error(request, 'you verification code not match')
#                     return redirect('verify')
#     return render(request, 'verify.html', {'form': form})
