from django import forms
from django.contrib.auth import get_user_model
from authentication.models import Profile

User = get_user_model()
from django.contrib.auth.forms import ReadOnlyPasswordHashField


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, error_messages={'password': 'password must match'})
    password_2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput,
                                 error_messages={'password': 'password must match'})

    class Meta:
        model = User
        fields = ['phone_number', 'name', 'password', 'password_2']

    def clean_phone(self):
        '''
        Verify phone is available.
        '''
        phone_number = self.cleaned_data.get('phone_number')
        name = self.cleaned_data.get('name')
        password = self.cleaned_data.get('password')
        qs = User.objects.filter(phone_number=phone_number, is_verified=True)
        if qs.exists():
            raise forms.ValidationError("phone number  is taken")

        return phone_number

    def clean(self):
        # verify both password
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_2 = cleaned_data.get("password_2")
        if password is not None and password != password_2:
            self.add_error("password_2", "Your passwords must match")
        return cleaned_data

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UserAdminCreationForm(forms.ModelForm):
    """
    A form for creating new users. Includes all the required
    fields, plus a repeated password.
    """
    password = forms.CharField(widget=forms.PasswordInput)
    password_2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['phone_number']

    def clean(self):
        '''
        Verify both passwords match.
        '''
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_2 = cleaned_data.get("password_2")
        if password is not None and password != password_2:
            self.add_error("password_2", "Your passwords must match")
        return cleaned_data

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ['name', 'phone_number', 'password', 'is_active', 'admin']

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


# form =========================== phone number =====================

class NewPinForm(forms.Form):
    phone_number = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)


class ResetPasswordForm(forms.Form):
    phone_number = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)


class PasswordConfirmForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput, error_messages={'password': 'password must match'})
    password_2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput,
                                 error_messages={'password': 'password must match'})

    class Meta:
        model = User
        fields = ['password', 'password_2', ]

    def clean(self):
        # verify both password
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_2 = cleaned_data.get("password_2")
        if password is not None and password != password_2:
            self.add_error("password_2", "Your passwords must match")
        return cleaned_data


# update profile ==================== update main profile

class UpdateMainForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'phone_number', ]


class UpdateProfileForm(forms.ModelForm):
    user_image = forms.ImageField(label='Profile picture', required=False)
    id_number = forms.IntegerField(label='ID number', required=False)
    date_of_birth = forms.DateField(
        widget=forms.TextInput(
            attrs={'type': 'date'}
        ),
        label='Date of Birth',
        required=False
    )
    email = forms.EmailField(label='Email', required=False)
    rank = forms.CharField(label='Rank', required=False)
    residence = forms.CharField(label='Residence', required=False)

    class Meta:
        model = Profile
        fields = ['user_image', 'date_of_birth', 'id_number', 'email', 'rank', 'residence', ]
