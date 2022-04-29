from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView


class SignupView(CreateView):
    form_class = UserCreationForm
    success_url = 'login'
    template_name = 'accounts/signup.html'


class AccountLoginView(LoginView):
    redirect_authenticated_user = True
    template_name = 'accounts/login.html'
