from django.shortcuts import render, get_object_or_404
from .models import *
from django.urls import reverse
from datetime import datetime
# Create your views here.

def main(request):
    now = datetime.now()
    return render(request, 'esl_app/main.html', {'time': now})

def login(request):
    now = datetime.now()
    return render(request, 'esl_app/login.html', {'time': now})

def login_forgot(request):
    now = datetime.now()
    return render(request, 'esl_app/forgot.html', {'time': now})

def register(request):
    now = datetime.now()
    return render(request, 'esl_app/register.html', {'time': now})

def profile(request):
    now = datetime.now()
    return render(request, 'esl_app/profile.html', {'time': now})

def profile_completed(request):
    now = datetime.now()
    return render(request, 'esl_app/completed.html', {'time': now})

def profile_options(request):
    now = datetime.now()
    return render(request, 'esl_app/options.html', {'time': now})

def test_list(request):
    now = datetime.now()
    return render(request, 'esl_app/tests.html', {'time': now})

def test(request):
    now = datetime.now()
    return render(request, 'esl_app/test.html', {'time': now})

def test_result(request):
    now = datetime.now()
    return render(request, 'esl_app/result.html', {'time': now})
