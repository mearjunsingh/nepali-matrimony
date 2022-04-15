from django.urls import path
from users import views as v


urlpatterns = [
    path('', v.update_user_profile, name='update_user_profile'),
    path('register/', v.register_user_profile, name='register_user_profile'),
    path('verify/', v.verify_user_profile, name='verify_user_profile'),
    path('save/', v.save_user_profile, name='save_user_profile'),
    path('activate/', v.activate_user_profile, name='activate_user_profile'),
    path('login/', v.login_user_profile, name='login_user_profile'),
    path('logout/', v.logout_user_profile, name='logout_user_profile')
]
