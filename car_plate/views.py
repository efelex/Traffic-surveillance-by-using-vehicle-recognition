from django.shortcuts import render, redirect, loader
from django.utils import timezone
from car_plate.plate_detection import plate_detect, automatic_detect
from car_plate.models import Car_registration, Insurance, Car_Control, Tax, Captured, Charged_car, Charged_car_official, \
    Dummy, Unregistered_car
from datetime import timedelta
from datetime import datetime
import cv2
import numpy as np

now = timezone.now()

future_date = datetime.now() + timedelta(days=3)
waranty_expire = future_date.date()


# Create your views here.

def detect_car(request):
    user = request.user
    plate_number = plate_detect()
    # plate_number = 'RAD666T'
    user_police_road = request.user  # police who is in the road
    # if plate number is not dummy
    if not plate_number == 'DUMMY':
        try:
            # try and check if plate number exist in database
            car_detected = Car_registration.objects.filter(plate_number=plate_number).first()
            # if plate exist in db
            if car_detected:
                plate_number_car = Car_registration.objects.filter(plate_number=plate_number).first().plate_number
                print("plate --number---", plate_number_car)

                # evaluating and see if this plate number exist in different database include tax, insu--, control --
                insurance_prof = Insurance.objects.filter(car__plate_number=plate_number_car).first()
                control_prof = Car_Control.objects.filter(car__plate_number=plate_number_car).first()
                tax_prof = Tax.objects.filter(car__plate_number=plate_number_car).first()

                # if plate number exist in insurance db
                if insurance_prof:
                    insurance_prof = insurance_prof.insurance_duration_end
                    # check and see if end time of insurance expired
                    if insurance_prof < now.date():
                        insurance_status = False
                        # give this plate number expire the date to be paid
                        insurance_waranty_new = waranty_expire
                        # print('insurance expired -------------------', insurance_status)
                    else:
                        insurance_status = True
                        insurance_waranty_new = None
                        # print('insurance live -------------------', insurance_status)
                # if plate number not exist in insurance db
                else:
                    insurance_status = False
                    insurance_waranty_new = waranty_expire
                    # print('Car not registered in any insurance -------------------', insurance_status)
                # if plate number exist in control db
                if control_prof:
                    control_prof = control_prof.control_end
                    # check and see if end time of control expired
                    if control_prof < now.date():
                        control_status = False
                        control_waranty_new = waranty_expire
                        # print("Control expired ------------------", control_status)
                    else:
                        control_status = True
                        control_waranty_new = None
                        # print("control live --------------------", control_status)
                # if plate number not exist in control db
                else:
                    control_status = False
                    control_waranty_new = waranty_expire
                    # print('Car not registered in any Control -------------------', control_status)
                # if plate number  exist in tax db
                if tax_prof:
                    tax_prof = tax_prof.tax_end

                    # check and see if end time of tax expired
                    if tax_prof < now.date():
                        tax_status = False
                        tax_waranty_new = waranty_expire

                        # print("Tax expired -----------------", tax_status)
                    else:
                        tax_status = True
                        tax_waranty_new = None
                        # print("Tax status -----------------------", tax_status)
                # if plate number not exist in tax db
                else:
                    tax_status = False
                    tax_waranty_new = waranty_expire
                    # print('Car not registered in any Tax -------------------', tax_status)

                result = Captured.objects.create(police=user, car=car_detected, insurance_status=insurance_status,
                                                 control_status=control_status, tax_status=tax_status)

                # ========================================== charging phase =======================================

                # if tax is false means that tax expired
                if not tax_status:
                    tax_charged = 500
                    charging = Charged_car.objects.filter(car=car_detected)
                    if charging:
                        Charged_car.objects.filter(car=car_detected).update(tax_charged=tax_charged,
                                                                            tax_ban_expire=tax_waranty_new)
                    else:
                        Charged_car.objects.create(police=user, car=car_detected, tax_charged=tax_charged,
                                                   tax_ban_expire=tax_waranty_new)
                else:
                    tax_charged = 0
                    charging = Charged_car.objects.filter(car=car_detected)
                    if charging:
                        Charged_car.objects.filter(car=car_detected).update(tax_charged=tax_charged,
                                                                            tax_ban_expire=tax_waranty_new)
                    else:
                        Charged_car.objects.create(police=user, car=car_detected, tax_charged=tax_charged,
                                                   tax_ban_expire=tax_waranty_new)
                # if insurance is false means that insurance expired
                if not insurance_status:
                    insurance_charged = 1000
                    charging = Charged_car.objects.filter(car=car_detected)
                    if charging:
                        Charged_car.objects.filter(car=car_detected).update(insurance_charged=insurance_charged,
                                                                            insurance_ban_expire=insurance_waranty_new)
                    else:
                        Charged_car.objects.create(police=user, car=car_detected, insurance_charged=insurance_charged,
                                                   insurance_ban_expire=insurance_waranty_new)
                else:
                    insurance_charged = 0
                    charging = Charged_car.objects.filter(car=car_detected)
                    if charging:
                        Charged_car.objects.filter(car=car_detected).update(insurance_charged=insurance_charged,
                                                                            insurance_ban_expire=insurance_waranty_new)
                    else:
                        Charged_car.objects.create(police=user, car=car_detected, insurance_charged=insurance_charged,
                                                   insurance_ban_expire=insurance_waranty_new)
                # if control is false means that control expired
                if not control_status:
                    control_charged = 1500
                    charging = Charged_car.objects.filter(car=car_detected)
                    if charging:
                        Charged_car.objects.filter(car=car_detected).update(control_charged=control_charged,
                                                                            control_ban_expire=control_waranty_new)
                    else:
                        Charged_car.objects.create(police=user, car=car_detected, control_charged=control_charged,
                                                   control_ban_expire=control_waranty_new)
                else:
                    control_charged = 0
                    charging = Charged_car.objects.filter(car=car_detected)
                    if charging:
                        Charged_car.objects.filter(car=car_detected).update(control_charged=control_charged,
                                                                            control_ban_expire=control_waranty_new)
                    else:
                        Charged_car.objects.create(police=user, car=car_detected, control_charged=control_charged,
                                                   control_ban_expire=control_waranty_new)

                '''
                we have different table captured =====> charged car then here it can be change overtime based on status from your insurance, tax, control information
                but we have another part which created automatically by signals called Charged_car_official table so here we have infor  for all car 
                and even it being changed when you paid the first charges 
                so down section prevent anyone who is charged then go maybe in insurance service then paid in order that when camera capture him it will change the charges
                so this section prevent those faults
                
                '''
                charged_offic_check = Charged_car_official.objects.filter(car=car_detected).first()
                charging_temporaly = Charged_car.objects.filter(car=car_detected).first()
                if charged_offic_check:
                    insurance_amount = charging_temporaly.insurance_charged
                    control_charged = charging_temporaly.control_charged
                    tax_charged = charging_temporaly.tax_charged
                    if charged_offic_check.insurance_charged_amount < insurance_amount:
                        insurance_amount = insurance_amount
                        insurance_exp = charging_temporaly.insurance_ban_expire
                    else:
                        insurance_amount = charged_offic_check.insurance_charged_amount
                        insurance_exp = charged_offic_check.insurance_tole_expire
                    if charged_offic_check.control_charged_amount < control_charged:
                        control_amount = control_charged
                        control_exp = charging_temporaly.control_ban_expire
                    else:
                        control_amount = charged_offic_check.control_charged_amount
                        control_exp = charged_offic_check.control_tole_expire
                    print("charged -----------------------", charged_offic_check.tax_charged_amount)
                    print("tax_charged ---------------------------------------------", tax_charged)
                    '''
                    here we used this expression different for other because this tax is created before the other one it make difficult
                    for our signal file py to update all data automatically sp we require another query to update to charged_car_official
                    so because here both charged car for tax and charged_car_official are valid it is difficult to say 500<500
                    so we use < or =
                    to keep working on our logic 
                    
                    '''
                    if charged_offic_check.tax_charged_amount < tax_charged or charged_offic_check.tax_charged_amount == tax_charged:
                        if charged_offic_check.tax_tole_expire:
                            tax_amount = tax_charged
                            tax_exp = charged_offic_check.tax_tole_expire
                        else:
                            tax_amount = tax_charged
                            tax_exp = charging_temporaly.tax_ban_expire
                    else:
                        tax_amount = charged_offic_check.tax_charged_amount
                        tax_exp = charged_offic_check.tax_tole_expire
                    Charged_car_official.objects.filter(car=car_detected).update(
                        insurance_charged_amount=insurance_amount,
                        tax_charged_amount=tax_amount,
                        control_charged_amount=control_amount, insurance_tole_expire=insurance_exp,
                        control_tole_expire=control_exp, tax_tole_expire=tax_exp)

                # ======================== check if car paid their charges with check waranty expiration
                # =======================
                check_car_charged_official = Charged_car_official.objects.filter(car=car_detected).first()
                if check_car_charged_official:
                    insurance_danger_check = check_car_charged_official.insurance_tole_expire
                    control_danger_check = check_car_charged_official.control_tole_expire
                    tax_danger_check = check_car_charged_official.tax_tole_expire
                    if insurance_danger_check:
                        if now.date() > insurance_danger_check:
                            return redirect('warning_danger',
                                            id=check_car_charged_official.id)  # danger screen and warning for this car
                    if control_danger_check:
                        if now.date() > control_danger_check:
                            return redirect('warning_danger', id=check_car_charged_official.id)
                    if tax_danger_check:
                        if now.date() > tax_danger_check:
                            return redirect('warning_danger', id=check_car_charged_official.id)



            # if plate not exist in db
            else:

                print("car not registered")
                # save car which is not registered with avoiding duplication
                check_unregistered = Unregistered_car.objects.filter(plate_number=plate_number).first()
                if check_unregistered:
                    Unregistered_car.objects.create(police=check_unregistered.police,
                                                    plate_number=check_unregistered.plate_number, danger=True)
                else:
                    Unregistered_car.objects.create(police=user_police_road, plate_number=plate_number, danger=True)

        # if is not exist in db say car is not registered and other condition or something went wrong
        except:
            print("car not registered or something went wrong")
    # else if is plate number dummy
    else:
        Dummy.objects.create(police=user_police_road)
        print("dummy")

    return redirect('dashboard')


def automatic_detect_car(request):
    user = request.user
    plate_number = automatic_detect()
    user_police_road = request.user  # police who is in the road
    # plate_number = 'RAD66T'
    if not plate_number == 'DUMMY':
        try:
            car_detected = Car_registration.objects.filter(plate_number=plate_number).first()
            if car_detected:
                plate_number_car = Car_registration.objects.filter(plate_number=plate_number).first().plate_number
                print("plate --number-- car----", plate_number_car)

                # ======= evaluating if this plate number are in insurance , tax, control

                insurance_prof = Insurance.objects.filter(car__plate_number=plate_number_car).first()
                control_prof = Car_Control.objects.filter(car__plate_number=plate_number_car).first()
                tax_prof = Tax.objects.filter(car__plate_number=plate_number_car).first()

                # if plate number exist in insurance database
                if insurance_prof:
                    insurance_prof = insurance_prof.insurance_duration_end
                    # check and see if end time of insurance expired maybe warranty
                    if insurance_prof < now.date():
                        insurance_status = False
                        # give this plate number expire the date to be paid
                        insurance_waranty_new = waranty_expire
                        # print('insurance expired -------------------', insurance_status)
                    else:
                        insurance_status = True
                        insurance_waranty_new = None
                        # print('insurance live -------------------', insurance_status)
                # if plate number not exist in insurance db
                else:
                    insurance_status = False
                    insurance_waranty_new = waranty_expire
                if control_prof:
                    control_prof = control_prof.control_end
                    # check and see if end time of control expired
                    if control_prof < now.date():
                        control_status = False
                        control_waranty_new = waranty_expire
                        # print("Control expired ------------------", control_status)
                    else:
                        control_status = True
                        control_waranty_new = None
                        # print("control live --------------------", control_status)
                # if plate number not exist in control db
                else:
                    control_status = False
                    control_waranty_new = waranty_expire
                # if plate number  exist in tax db
                if tax_prof:
                    tax_prof = tax_prof.tax_end

                    # check and see if end time of tax expired
                    if tax_prof < now.date():
                        tax_status = False
                        tax_waranty_new = waranty_expire

                        # print("Tax expired -----------------", tax_status)
                    else:
                        tax_status = True
                        tax_waranty_new = None
                        # print("Tax status -----------------------", tax_status)
                # if plate number not exist in tax db
                else:
                    tax_status = False
                    tax_waranty_new = waranty_expire

                result = Captured.objects.create(police=user, car=car_detected, insurance_status=insurance_status,
                                                 control_status=control_status, tax_status=tax_status)
                # ====================== charging phase for car =======================================

                # if tax is false means that tax expired
                if not tax_status:
                    tax_charged = 500
                    charging = Charged_car.objects.filter(car=car_detected)
                    if charging:
                        Charged_car.objects.filter(car=car_detected).update(tax_charged=tax_charged,
                                                                            tax_ban_expire=tax_waranty_new)
                    else:
                        Charged_car.objects.create(police=user, car=car_detected, tax_charged=tax_charged,
                                                   tax_ban_expire=tax_waranty_new)

                else:
                    tax_charged = 0
                    charging = Charged_car.objects.filter(car=car_detected)
                    if charging:
                        Charged_car.objects.filter(car=car_detected).update(tax_charged=tax_charged,
                                                                            tax_ban_expire=tax_waranty_new)
                    else:
                        Charged_car.objects.create(police=user, car=car_detected, tax_charged=tax_charged,
                                                   tax_ban_expire=tax_waranty_new)

                # if insurance is false means that insurance expired
                if not insurance_status:
                    insurance_charged = 1000
                    charging = Charged_car.objects.filter(car=car_detected)
                    if charging:
                        Charged_car.objects.filter(car=car_detected).update(insurance_charged=insurance_charged,
                                                                            insurance_ban_expire=insurance_waranty_new)
                    else:
                        Charged_car.objects.create(police=user, car=car_detected, insurance_charged=insurance_charged,
                                                   insurance_ban_expire=insurance_waranty_new)
                else:
                    insurance_charged = 0
                    charging = Charged_car.objects.filter(car=car_detected)
                    if charging:
                        Charged_car.objects.filter(car=car_detected).update(insurance_charged=insurance_charged,
                                                                            insurance_ban_expire=insurance_waranty_new)
                    else:
                        Charged_car.objects.create(police=user, car=car_detected, insurance_charged=insurance_charged,
                                                   insurance_ban_expire=insurance_waranty_new)
                # if control is false means that control expired
                if not control_status:
                    control_charged = 1500
                    charging = Charged_car.objects.filter(car=car_detected)
                    if charging:
                        Charged_car.objects.filter(car=car_detected).update(control_charged=control_charged,
                                                                            control_ban_expire=control_waranty_new)
                    else:
                        Charged_car.objects.create(police=user, car=car_detected, control_charged=control_charged,
                                                   control_ban_expire=control_waranty_new)
                else:
                    control_charged = 0
                    charging = Charged_car.objects.filter(car=car_detected)
                    if charging:
                        Charged_car.objects.filter(car=car_detected).update(control_charged=control_charged,
                                                                            control_ban_expire=control_waranty_new)
                    else:
                        Charged_car.objects.create(police=user, car=car_detected, control_charged=control_charged,
                                                   control_ban_expire=control_waranty_new)

                '''
                we have different table captured =====> charged car then here it can be change overtime based on status from your insurance, tax, control information
                but we have another part which created automatically by signals called Charged_car_official table so here we have infor  for all car
                and even it being changed when you paid the first charges
                so down section prevent anyone who is charged then go maybe in insurance service then paid in order that when camera capture him it will change the charges
                so this section prevent those faults

                '''
                charged_offic_check = Charged_car_official.objects.filter(car=car_detected).first()
                charging_temporaly = Charged_car.objects.filter(car=car_detected).first()
                if charged_offic_check:
                    insurance_amount = charging_temporaly.insurance_charged
                    control_charged = charging_temporaly.control_charged
                    tax_charged = charging_temporaly.tax_charged
                    if charged_offic_check.insurance_charged_amount < insurance_amount:
                        insurance_amount = insurance_amount
                        insurance_exp = charging_temporaly.insurance_ban_expire
                    else:
                        insurance_amount = charged_offic_check.insurance_charged_amount
                        insurance_exp = charged_offic_check.insurance_tole_expire
                    if charged_offic_check.control_charged_amount < control_charged:
                        control_amount = control_charged
                        control_exp = charging_temporaly.control_ban_expire
                    else:
                        control_amount = charged_offic_check.control_charged_amount
                        control_exp = charged_offic_check.control_tole_expire
                    print("charged -----------------------", charged_offic_check.tax_charged_amount)
                    print("tax_charged ---------------------------------------------", tax_charged)
                    '''
                    here we used this expression different for other because this tax is created before the other one it make difficult
                    for our signal file py to update all data automatically sp we require another query to update to charged_car_official
                    so because here both charged car for tax and charged_car_official are valid it is difficult to say 500<500
                    so we use < or =
                    to keep working on our logic

                    '''
                    if charged_offic_check.tax_charged_amount < tax_charged or charged_offic_check.tax_charged_amount == tax_charged:
                        if charged_offic_check.tax_tole_expire:
                            tax_amount = tax_charged
                            tax_exp = charged_offic_check.tax_tole_expire
                        else:
                            tax_amount = tax_charged
                            tax_exp = charging_temporaly.tax_ban_expire
                    else:
                        tax_amount = charged_offic_check.tax_charged_amount
                        tax_exp = charged_offic_check.tax_tole_expire
                    Charged_car_official.objects.filter(car=car_detected).update(
                        insurance_charged_amount=insurance_amount,
                        tax_charged_amount=tax_amount,
                        control_charged_amount=control_amount, insurance_tole_expire=insurance_exp,
                        control_tole_expire=control_exp, tax_tole_expire=tax_exp)
            # if plate number not exist in our database
            else:
                # here we are avoiding duplication
                check_unregistered = Unregistered_car.objects.filter(plate_number=plate_number).first()
                if check_unregistered:
                    Unregistered_car.objects.create(police=check_unregistered.police,
                                                    plate_number=check_unregistered.plate_number, danger=True)
                else:
                    Unregistered_car.objects.create(police=user_police_road, plate_number=plate_number, danger=True)
        except Exception as e:
            print(e)
    else:
        Dummy.objects.create(police=user_police_road)
        print("dummy")
    return redirect('automatic_detect_car')
