from django.contrib.auth.views import LoginView


class LoginPageView(LoginView):
    template_name = 'index.html'
    # form_class = LoginForm
    # success_url = reverse_lazy('user_dashboard')
    # redirect_authenticated_user = True
    # extra_context = {'mode' : 'login'}