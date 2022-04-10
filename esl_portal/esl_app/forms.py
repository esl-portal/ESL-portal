from .models import *
from .validators import *
from django import forms
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class UserLoginForm(forms.Form):
    username = forms.CharField(label='Введите имя пользователя', max_length=150, validators=[validate_username], error_messages={'required': 'Данное поле является обязательным для заполнения'})
    password = forms.CharField(label='Введите пароль', widget=forms.PasswordInput, validators=[validate_password], error_messages={'required': 'Данное поле является обязательным для заполнения'})


class UserForgotForm(forms.Form):
    username = forms.CharField(label="Введите имя пользователя", max_length=150, validators=[validate_username], error_messages={'required': 'Данное поле является обязательным для заполнения'})
    password = forms.CharField(label="Введите новый пароль", widget=forms.PasswordInput, validators=[validate_password], error_messages={'required': 'Данное поле является обязательным для заполнения'})
    password_confirmation = forms.CharField(label="Введите новый пароль ещё раз", widget=forms.PasswordInput, error_messages={'required': 'Данное поле является обязательным для заполнения'})


class UserRegistrationForm(forms.Form):
    username = forms.CharField(label='Имя пользователя', max_length=150, validators=[validate_username], error_messages={'required': 'Данное поле является обязательным для заполнения'})
    first_name = forms.CharField(label='Ваше имя', validators=[validate_firstname], error_messages={'required': 'Данное поле является обязательным для заполнения'})
    email = forms.EmailField(label='Адрес электронной почты', widget=forms.EmailInput, validators=[validate_email], error_messages={'required': 'Данное поле является обязательным для заполнения', 'invalid': 'Некорректный формат адреса электронной почты'})
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput, validators=[validate_password], error_messages={'required': 'Данное поле является обязательным для заполнения'})
    password2 = forms.CharField(label='Введите пароль ещё раз', widget=forms.PasswordInput, error_messages={'required': 'Данное поле является обязательным для заполнения'})

    def unique(self):
        return not User.objects.filter(username=self.cleaned_data['username']).exists()

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not validate_email(email):
            raise ValidationError(
                message=_('Некорректный формал email'),
                code='email',
                params={'email': email}
            )
        return email

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not validate_firstname(first_name):
            raise ValidationError(
                message=_('Некорректный формат имени'),
                code='firstname',
                params={'firstname': first_name}
            )
        return first_name

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not validate_username(username):
            raise ValidationError(
                message=_('Некорректный формат никнейма'),
                code='username',
                params={'username': username}
            )
        return username

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not validate_password(password):
            raise ValidationError(
                message=_('Некорректный формат пароля'),
                code='password',
            )
        return password

    def clean_password2(self):
        password2 = self.cleaned_data.get('password2')
        if not (password2 == self.cleaned_data.get('password')):
            raise ValidationError(
                message=_('Пароли не совпадают'),
                code='password',
            )
        return password2


class UserChangeData(forms.Form):
    new_username = forms.CharField(label='Имя пользователя', max_length=50, validators=[validate_username])
    new_first_name = forms.CharField(label='Ваше имя', validators=[validate_firstname])
    new_email = forms.EmailField(label='Адрес электронной почты', widget=forms.EmailInput, validators=[validate_email])
    new_password = forms.CharField(label='Новый пароль', widget=forms.PasswordInput, required=False, validators=[validate_password])