from django.urls import path
from . import views

urlpatterns = [
    path('main/', views.main, name='main'),
    path('login/', views.login, name='login'),
    path('login/forgot', views.login_forgot, name='login_forgot'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('profile/completed/', views.profile_completed, name='profile_completed'),
    path('profile/options/', views.profile_options, name='profile_options'),
    path('tests/', views.test_list, name='test_list'),
    path('test/<int:test_id>/', views.test, name='test'),
    path('test/<int:test_id>/result/', views.test_result, name='test_result'),
]