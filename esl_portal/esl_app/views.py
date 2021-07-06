from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.auth import authenticate, login
# Create your views here.

def main(request):
    return render(request, 'esl_app/main.html', {'auth': request.user.is_authenticated})

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
    now = 14141414
    return render(request, 'esl_app/forgot.html', {'time': now})

def register(request):
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
def profile(request):
    return render(request, 'esl_app/profile.html', {'user': request.user})

def profile_completed(request):
    now = datetime.now()
    return render(request, 'esl_app/completed.html', {'time': now})

def profile_options(request):
    now = datetime.now()
    return render(request, 'esl_app/options.html', {'time': now})

def test_list(request):
    list_of_tests = get_list_or_404(Test.objects.all())
    return render(request, 'esl_app/tests.html', {'list': list_of_tests})

def test(request, test_id):
    some_test = get_object_or_404(Test, pk=test_id)
    questions = some_test.questions.all()
    return render(request, 'esl_app/some_test.html', {'some_test': some_test,
                                                      'questions': questions})

def test_result(request):
    now = datetime.now()
    return render(request, 'esl_app/result.html', {'time': now})
