from .models import *
from django import forms
from django.contrib.auth.models import User


class UserLoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Подтвердите пароль', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'email']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают')

        return cd['password2']

class UserForgotForm(forms.Form):
    username = forms.CharField(label="Введите имя пользователя", max_length=150)
    password = forms.CharField(label="Введите новый пароль", widget=forms.PasswordInput)
    password_confirmation = forms.CharField(label="Введите новый пароль ещё раз",
                                            widget=forms.PasswordInput)