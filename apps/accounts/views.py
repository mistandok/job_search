from django.contrib.auth.views import LoginView
from django.views.generic import CreateView

from .forms import AccountUserCreationForm, AccountAuthenticationForm


class SignupView(CreateView):
    form_class = AccountUserCreationForm
    success_url = '/login'
    template_name = 'accounts/signup.html'


class AccountLoginView(LoginView):
    form_class = AccountAuthenticationForm
    redirect_authenticated_user = True
    template_name = 'accounts/login.html'
