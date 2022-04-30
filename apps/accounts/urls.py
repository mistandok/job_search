from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import SignupView, AccountLoginView

urlpatterns = [
    path('login/', AccountLoginView.as_view(next_page='start_page'), name='login'),
    path('register/', SignupView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(next_page='start_page'), name='logout', ),
]
