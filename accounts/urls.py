# accounts/urls.py
from django.urls import path
from . import auth

urlpatterns = [
    path('register/', auth.register_user, name='register'),
    path('login/', auth.login_user_view, name='login'),
    path('logout/', auth.logout_user_view, name='logout'),
]
