from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from .forms import *
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import models
# Create your views here.


def main(request):
    context = {'is_authenticated': request.user.is_authenticated, 'request': request}
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
            empty_form = UserLoginForm()
            return render(request, 'esl_app/login.html', {'wrong_credentials': True, 'form': empty_form})
    else:
        if request.user.is_authenticated:
            return redirect('/main/')
        else:
            empty_form = UserLoginForm()
            return render(request, 'esl_app/login.html', {'wrong_credentials': False, 'form': empty_form})


def login_forgot(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        password_confirmation = request.POST['password_confirmation']
        try:
            user = User.objects.get(username=username)
            if password == password_confirmation:
                user.set_password(password)
                user.save()
                return redirect(to='/login/')
            else:
                form = UserForgotForm(request.POST)
                return render(request, 'esl_app/forgot.html', {'wrong_credentials': True, 'form': form})
        except models.Model.DoesNotExist:
            form = UserForgotForm(request.POST)
            return render(request, 'esl_app/forgot.html', {'wrong_credentials': True, 'form': form})
    else:
        if request.user.is_authenticated:
            return redirect('/main/')
        else:
            form = UserForgotForm()
            return render(request, 'esl_app/forgot.html', {'wrong_credentials': False, 'form': form})


def register(request):
    pass


def profile(request):
    pass


@login_required(login_url='/login/')
def profile_completed(request):
    user = request.user
    completions = Completion.objects.filter(user=user)
    is_empty = len(completions) == 0
    return render(request, 'esl_app/completed.html', {'completions': completions, 'is_empty': is_empty})


def profile_options(request):
    pass


def test_list(request):
    pass


def test(request):
    pass


@login_required(login_url='/login/')
def test_result(request, test_id):
    completion = Completion.objects.filter(user=request.user, test_id=test_id)
    return render(request, 'esl_app/completed.html', {'completion': completion})


def log_out(request):
    logout(request)
    return redirect(to='/main/')
