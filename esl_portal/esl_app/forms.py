from .models import *
from django.forms import ModelForm
from django import forms


class UserLoginForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']


class UserForgotForm(forms.Form):
    username = forms.CharField(label="Введите имя пользователя", max_length=150)
    password = forms.CharField(label="Введите новый пароль", widget=forms.PasswordInput)
    password_confirmation = forms.CharField(label="Введите новый пароль ещё раз", widget=forms.PasswordInput)
