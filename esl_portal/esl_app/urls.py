from django.urls import path
from . import views


urlpatterns = [
    path('main/', views.main, name='main'),
    path('login/', views.log_in, name='login'),
    path('login/forgot', views.login_forgot, name='forgot'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('profile/completed/', views.profile_completed, name='completed'),
    path('profile/options/', views.profile_options, name='options'),
    path('tests/', views.test_list, name='tests'),
    path('tests/<int:test_id>', views.test, name='test'),
    path('tests/<int:test_id>/result', views.test_result, name='result'),
]
