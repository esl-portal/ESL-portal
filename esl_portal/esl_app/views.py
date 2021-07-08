from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
# Create your views here.

def main(request):
    return render(request, 'esl_app/main.html', {'auth': request.user.is_authenticated,
                                                 'request': request})

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
            return render(request, 'esl_app/login.html', {'wrong_credentials': True,
                                                          'form': form})
    else:
        if request.user.is_authenticated:
            return redirect('/main/')
        else:
            form = UserLoginForm()
            return render(request, 'esl_app/login.html', {'wrong_credentials': False,
                                                          'form': form})


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
                return render(request, 'esl_app/forgot.html', {'wrong_credentials': True,
                                                               'form': form})
        except models.Model.DoesNotExist:
            form = UserForgotForm(request.POST)
            return render(request, 'esl_app/forgot.html', {'wrong_credentials': True,
                                                           'form': form})
    else:
        if request.user.is_authenticated:
            return redirect('/main/')
        else:
            form = UserForgotForm()
            return render(request, 'esl_app/forgot.html', {'wrong_credentials': False,
                                                           'form': form})

def log_out(request):
    logout(request)
    return redirect('/main/')

def register(request):
    if request.user.is_authenticated:
        return redirect('/main/')
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid() and (request.POST['password'] == request.POST['password2']) and user_form.unique():
            new_user = User(username=request.POST['username'],
                            first_name=request.POST['first_name'],
                            email=request.POST['email'],
                            password=request.POST['password'])
            new_user.save()
            return redirect('/login/')
    else:
        user_form = UserRegistrationForm()
    return render(request, 'esl_app/register.html', {'user_form': user_form})


@login_required(login_url='/login/')
def profile(request):
    return render(request, 'esl_app/profile.html', {'user': request.user})

@login_required(login_url='/login/')
def profile_completed(request):
    user = request.user
    completions = Completion.objects.filter(user=user)
    is_empty = len(completions) == 0
    return render(request, 'esl_app/completed.html', {'completions': completions,
                                                      'is_empty': is_empty})

@login_required(login_url='/login/')
def profile_options(request):
    user = request.user
    if request.method == 'POST':
        form = UserChangeData(request.POST)
        if form.is_valid():
            new_username = request.POST['new_username']
            new_email = request.POST['new_email']
            new_first_name = request.POST['new_first_name']
            if user.username != new_username:
                user.username = new_username
            if user.email != new_email:
                user.email = new_email
            if user.first_name != new_first_name:
                user.first_name = new_first_name
            if request.POST['new_password'] != '':
                user.set_password(request.POST['new_password'])
            user.save()
            return redirect('/profile/')
    else:
        data = {'new_username': user.username,
                'new_first_name': user.first_name,
                'new_email': user.email}
        form = UserChangeData(initial=data)
    return render(request, 'esl_app/options.html', {'user': request.user,
                                                    'form': form})

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
