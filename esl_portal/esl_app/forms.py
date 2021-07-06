from .models import *
from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User


class UserLoginForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']

class UserRegistrationForm(ModelForm):
    password = forms.Charfield(label='Password', widget=forms.PasswordInput)
    password2 = forms.Charfield(label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'email']

    def clean_passwords(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают')

        return cd['password2']