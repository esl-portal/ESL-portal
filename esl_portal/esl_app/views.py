from django.shortcuts import render, get_object_or_404
from .models import *
from django.urls import reverse
# Create your views here.


def main(request):
    context = {'is_authenticated': request.user.is_authenticated}
    return render(request, 'esl_app/main.html', context)


def login(request):
    pass


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
