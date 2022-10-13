from django.urls import path

from .views import *

urlpatterns = [
    path("", update_user_profile, name="update_user_profile"),
    path("register/", register_user_profile, name="register_user_profile"),
    path("login/", login_user_profile, name="login_user_profile"),
    path("logout/", logout_user_profile, name="logout_user_profile"),
]
