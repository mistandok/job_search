"""
Модуль отвечает за вспомогательные классы и функции для навигации на сайте
"""
from abc import ABC, abstractmethod

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect

from ..models import Company, Vacancy, Resume


class ObjectExistForUserChecker(ABC):
    """
    Класс должен осуществлять проверку на то, что интересуемый объект существует для пользователя
    """
    @abstractmethod
    def __call__(self, user: User) -> bool:
        """
        Метод проверяет, что для пользователя существует требуемый объект.
        """
        pass


class CompanyExistForUserChecker(ObjectExistForUserChecker):
    """
    Класс проверяет, что для пользователя существует компания.
    """
    def __call__(self, user: User):
        try:
            Company.objects.get(owner=user)
            return True
        except ObjectDoesNotExist:
            return False


class VacancyExistForUserChecker(ObjectExistForUserChecker):
    """
    Класс проверяет, что для пользователя существуют вакансии.
    """
    def __call__(self, user: User):
        if Vacancy.objects.filter(company__owner=user).exists():
            return True
        return False


class ResumeExistForUserChecker(ObjectExistForUserChecker):
    """
    Класс проверяет, что для пользователя существует резюме.
    """
    def __call__(self, user: User):
        try:
            Resume.objects.get(owner=user)
            return True
        except ObjectDoesNotExist:
            return False


def redirect_for_user(
        is_object_should_exist: bool,
        redirect_to: str,
        object_exists_checker: ObjectExistForUserChecker
):
    """
    Декоратор отвечает за перенаправление запросов для вьюх. Вешается на метод Get
    :param is_object_should_exist:
    True - для перенаправления на новую View объект должен существовать для пользователя
    False - для перенаправления на новую View объект не должен сущуствовать для пользователя
    :param redirect_to: название View, куда нужно перенаправть запрос.
    :param object_exists_checker: проверяет, что объект существует для пользователя
    """
    def decorator(func):
        def wrapper(request, *args, **kwargs):
            is_object_exists = object_exists_checker(request.user)
            if is_object_should_exist:
                return redirect(redirect_to) if is_object_exists else func(request, *args, **kwargs)
            else:
                return func(request, *args, **kwargs) if is_object_exists else redirect(redirect_to)

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

