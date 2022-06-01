from django import forms
from admin_panel.models import Send_message


class Admin_send_messageForm(forms.ModelForm):
    class Meta:
        model = Send_message
        fields = ['subject_message', 'body_message', ]
