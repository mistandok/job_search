"""
Модуль отвечает за вспомогательные классы и функции для навигации на сайте
"""
from abc import ABC, abstractmethod

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect

from ..models import Company, Vacancy, Resume


class ObjectExistForUserChecker(ABC):
    @abstractmethod
    def __call__(self, user: User):
        pass


class CompanyExistForUserChecker(ObjectExistForUserChecker):
    def __call__(self, user: User):
        try:
            Company.objects.get(owner=user)
            return True
        except ObjectDoesNotExist:
            return False


class VacancyExistForUserChecker(ObjectExistForUserChecker):
    def __call__(self, user: User):
        if Vacancy.objects.filter(company__owner=user).exists():
            return True
        return False


class ResumeExistForUserChecker(ObjectExistForUserChecker):
    def __call__(self, user: User):
        try:
            Resume.objects.get(user=user)
            return True
        except ObjectDoesNotExist:
            return False


def redirect_for_user(
        is_object_should_exist: bool,
        redirect_to: str,
        object_exists_for_user_checker: ObjectExistForUserChecker
):
    """
    Декоратор отвечает за перенаправление запросов для вьюх. Вешается на метод Get
    :param is_object_should_exist:
    True - для перенаправления на новую View объект должен существовать для пользователя
    False - для перенаправления на новую View объект не должен сущуствовать для пользователя
    :param redirect_to: название View, куда нужно перенаправть запрос.
    :param object_exists_for_user_checker: проверяет, что объект существует для пользователя
    """
    def decorator(func):
        def wrapper(self, request, *args, **kwargs):
            is_object_exists = object_exists_for_user_checker(request.user)
            if is_object_should_exist:
                return redirect(redirect_to) if is_object_exists else func(self, request, *args, **kwargs)
            else:
                return func(self, request, *args, **kwargs) if is_object_exists else redirect(redirect_to)

        return wrapper
    return decorator


def is_correct_company_for_user(company: Company, user: User):
    """
    Функция проверяет принадлежит ли компания пользователю
    :param company: компания
    :param user: пользователь
    """
    try:
        if company != Company.objects.get(owner=user):
            return False
    except ObjectDoesNotExist:
        return False
    return True

