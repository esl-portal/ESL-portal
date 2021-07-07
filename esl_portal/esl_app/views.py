from django.shortcuts import render, get_object_or_404, redirect, get_list_or_404
from .models import *
from django.contrib.auth.decorators import login_required
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


def log_out(request):
    logout(request)
    return redirect('/main/')

def register(request):
    if request.user.is_authenticated:
        return redirect('/main/')
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid() and user_form.clean_password2():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            return redirect('/login/')
    else:
        user_form = UserRegistrationForm()
    return render(request, 'esl_app/register.html', {'user_form': user_form})


@login_required(login_url='/login/')
def profile_completed(request):
    user = request.user
    completions = Completion.objects.filter(user=user)
    is_empty = len(completions) == 0
    return render(request, 'esl_app/completed.html', {'completions': completions, 'is_empty': is_empty})


def profile_options(request):
    pass


def test_list(request):
    list_of_tests = get_list_or_404(Test.objects.all())
    return render(request, 'esl_app/tests.html', {'list': list_of_tests})

def test(request, test_id):
    some_test = get_object_or_404(Test, pk=test_id)
    questions = some_test.questions.all()
    return render(request, 'esl_app/some_test.html', {'some_test': some_test,
                                                      'questions': questions})


@login_required(login_url='/login/')
def test_result(request, test_id):
    completion = Completion.objects.filter(user=request.user, test_id=test_id)
    return render(request, 'esl_app/completed.html', {'completion': completion})
