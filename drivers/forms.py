from django import forms
from django.core.exceptions import ValidationError
from car_plate.models import Car_registration


class LoginDriverForm(forms.Form):
    username = forms.CharField(max_length=25)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        owner_car = Car_registration.objects.filter(owner_phone_number=username)
        if not username.startswith("+"):
            raise forms.ValidationError("phone number must start with + and country code")
        elif not owner_car:
            raise forms.ValidationError("Car registration with this phone number not exist")
        return username


class VerifyPinForm(forms.Form):
    number_code = forms.IntegerField()

    def clean_number_code(self):
        number_code = self.cleaned_data.get('number_code')
        # print("number -----------------", number_code)
        # print("count number ---------------", len(str(number_code)))
        if len(str(number_code)) <= 3:
            raise forms.ValidationError("pin must equal to 5 number")
        return number_code


class CarAssignForm(forms.ModelForm):
    class Meta:
        model = Car_registration
        fields = ['phone_number_assign', ]

