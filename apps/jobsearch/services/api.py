"""
Модуль отвечает за API приложения.
"""

__author__ = 'Artikov A.K.'

from typing import List

from django.db.models import QuerySet, Q

from apps.jobsearch.models import Vacancy


def get_vacancies_by_search_filter(search_filter: str) -> QuerySet:
    if search_filter:
        fields_for_search = (
            'title',
            'skills',
            'description',
            'company__description',
            'company__name',
            'company__location',
            'specialty__title',
            'specialty__code',
        )
        q_filter = _get_q_contains_filter_for_fields_and_filter(fields_for_search, search_filter)
        return Vacancy.objects.filter(q_filter)

    return Vacancy.objects.all()


def _get_q_contains_filter_for_fields_and_filter(fields: List[str], search_filter: str) -> Q:
    q_filter = Q()
    for field in fields:
        param = {f'{field}__icontains': search_filter}
        q_filter |= Q(**param)
    return q_filter
