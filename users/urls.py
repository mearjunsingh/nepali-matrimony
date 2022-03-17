from django.urls import path
from users.views import LoginPageView


urlpatterns = [
    path('login/', LoginPageView.as_view(), name='login_page'),
]
