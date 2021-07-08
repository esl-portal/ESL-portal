from .models import *
from django import forms
from django.contrib.auth.models import User


class UserLoginForm(forms.Form):
    username = forms.CharField(label='Введите имя пользователя', max_length=150)
    password = forms.CharField(label='Введите пароль', widget=forms.PasswordInput)


class UserForgotForm(forms.Form):
    username = forms.CharField(label="Введите имя пользователя", max_length=150)
    password = forms.CharField(label="Введите новый пароль", widget=forms.PasswordInput)
    password_confirmation = forms.CharField(label="Введите новый пароль ещё раз", widget=forms.PasswordInput)


class UserRegistrationForm(forms.Form):
    username = forms.CharField(label='Имя пользователя', max_length=150)
    first_name = forms.CharField(label='Ваше имя')
    email = forms.EmailField(label='Адрес электронной почты', widget=forms.EmailInput)
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Введите пароль ещё раз', widget=forms.PasswordInput)

    def unique(self):
        return not User.objects.filter(username=self.cleaned_data['username']).exists()

class UserChangeData(forms.Form):
    new_username = forms.CharField(label='Имя пользователя', max_length=50)
    new_first_name = forms.CharField(label='Ваше имя')
    new_email = forms.EmailField(label='Адрес электронной почты', widget=forms.EmailInput)
    new_password = forms.CharField(label='Новый пароль', widget=forms.PasswordInput, required=False)
