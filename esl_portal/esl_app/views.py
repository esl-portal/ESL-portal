from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from .forms import *
from django.urls import reverse
from django.contrib.auth import authenticate, login
# Create your views here.


def main(request):
    context = {'is_authenticated': request.user.is_authenticated}
    return render(request, 'esl_app/main.html', context)


def log_in(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request=request, user=user)
            return redirect('/main/')
        else:
            form = UserLoginForm()
            return render(request, 'esl_app/login.html', {'wrong_credentials': True, 'form': form})
    else:
        if request.user.is_authenticated:
            return redirect('/main/')
        else:
            form = UserLoginForm()
            return render(request, 'esl_app/login.html', {'wrong_credentials': False, 'form': form})


def login_forgot(request):
    pass


def register(request):
    pass


def profile(request):
    pass


def profile_completed(request):
    pass


def profile_options(request):
    pass


def test_list(request):
    pass


def test(request):
    pass


def test_result(request):
    pass


def result(request):
    pass
