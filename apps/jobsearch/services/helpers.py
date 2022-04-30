"""
Модуль отвечает за вспомогательные классы и функции.
"""

from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect

from ..models import Company


def my_company_redirect_for_user(is_company_should_exist: bool, redirect_to: str):
    """
    Декоратор отвечает за перенаправление запросов для вьюх MyCompany.
    :param is_company_should_exist:
    True - для перенаправления на новую View компания должна существовать для пользователя
    False - для перенаправления на новую View компании не должна сущуствовать для пользователя
    :param redirect_to: название View, куда нужно перенаправть запрос.
    """
    def decorator(func):
        def wrapper(self, request, *args, **kwargs):
            try:
                Company.objects.get(owner=request.user)
                return redirect(redirect_to) if is_company_should_exist else func(self, request, *args, **kwargs)
            except ObjectDoesNotExist:
                return func(self, request, *args, **kwargs) if is_company_should_exist else redirect(redirect_to)

        return wrapper
    return decorator
