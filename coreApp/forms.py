from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class DateTimeInput(forms.DateTimeInput):
    input_type = 'datetime-local'

class AddQueryForm(forms.ModelForm):
     class Meta:
         model = Query
         fields = ('business', 'recordDate', 'master', 'service', 'phone')
         widgets = {
             'recordDate': DateTimeInput()
         }

class UserDataProfileForm(forms.ModelForm):
    class Meta:
        model = UserDataProfile
        fields = ('avatar',)


class NewUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password1", "password2")

