from .models import *
from .validators import *
from django import forms
from django.contrib.auth.models import User


class UserLoginForm(forms.Form):
    username = forms.CharField(label='Введите имя пользователя', max_length=150, validators=[validate_username])
    password = forms.CharField(label='Введите пароль', widget=forms.PasswordInput, validators=[validate_password])


class UserForgotForm(forms.Form):
    username = forms.CharField(label="Введите имя пользователя", max_length=150, validators=[validate_username])
    password = forms.CharField(label="Введите новый пароль", widget=forms.PasswordInput, validators=[validate_password])
    password_confirmation = forms.CharField(label="Введите новый пароль ещё раз", widget=forms.PasswordInput)


class UserRegistrationForm(forms.Form):
    username = forms.CharField(label='Имя пользователя', max_length=150, validators=[validate_username])
    first_name = forms.CharField(label='Ваше имя')
    email = forms.EmailField(label='Адрес электронной почты', widget=forms.EmailInput, validators=[validate_email_form])
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput, validators=[validate_password])
    password2 = forms.CharField(label='Введите пароль ещё раз', widget=forms.PasswordInput)

    def unique(self):
        return not User.objects.filter(username=self.cleaned_data['username']).exists()


class UserChangeData(forms.Form):
    new_username = forms.CharField(label='Имя пользователя', max_length=50, validators=[validate_username])
    new_first_name = forms.CharField(label='Ваше имя')
    new_email = forms.EmailField(label='Адрес электронной почты', widget=forms.EmailInput, validators=[validate_email_form])
    new_password = forms.CharField(label='Новый пароль', widget=forms.PasswordInput, required=False, validators=[validate_password])