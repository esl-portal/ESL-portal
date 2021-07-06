from .models import *
from django.forms import ModelForm


class UserLoginForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']
