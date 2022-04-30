"""
Модуль отвечает за вспомогательные классы и функции.
"""

from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect

from ..models import Company, Vacancy


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


def my_vacancy_redirect_for_user(is_vacancies_should_exist: bool, redirect_to: str):
    """
    Декоратор отвечает за перенаправление запросов для вьюх MyCompany.
    :param is_vacancies_should_exist:
    True - для перенаправления на новую View вакансии должны существовать для пользователя
    False - для перенаправления на новую View вакансии не должна сущуствовать для пользователя
    :param redirect_to: название View, куда нужно перенаправть запрос.
    """
    def decorator(func):
        def wrapper(self, request, *args, **kwargs):
            count_vacancies = Vacancy.objects.filter(company__owner=request.user).count()
            if count_vacancies:
                return redirect(redirect_to) if is_vacancies_should_exist else func(self, request, *args, **kwargs)
            return func(self, request, *args, **kwargs) if is_vacancies_should_exist else redirect(redirect_to)
        return wrapper
    return decorator
