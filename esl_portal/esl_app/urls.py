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
    path('tests/<int:test_id>/', views.test, name='test'),
    path('tests/<int:test_id>/result/', views.test_result, name='result'),
    path('logout/', views.log_out, name='logout'),
    path('tests/<int:test_id>/ajax/start/', views.start_test, name='start_test'),
    path('tests/<int:test_id>/ajax/next/', views.next_question, name='next_question'),
    path('tests/<int:test_id>/ajax/previous/', views.previous_question, name='previous_question'),
    path('tests/<int:test_id>/ajax/respond/', views.respond, name='respond'),
    path('tests/<int:test_id>/ajax/finish/', views.finish_test, name='finish_test')
]
