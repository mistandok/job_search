from django.contrib import admin
from django.urls import path

from apps.jobsearch.views import (
    StartPageView, ListVacancyView, DetailVacancyView, DetailCompanyView, ListSpecialtyVacancyView, ApplicationView
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', StartPageView.as_view(), name='start_page'),
    path('vacancies/', ListVacancyView.as_view(), name='all_vacancies'),
    path('vacancies/cat/<str:specialty>', ListSpecialtyVacancyView.as_view(), name='vacancies_for_specialty'),
    path('vacancies/<int:pk>', DetailVacancyView.as_view(), name='vacancy_detail'),
    path('vacancies/<int:pk>/send', ApplicationView.as_view(), name='application_sended'),
    path('companies/<int:pk>', DetailCompanyView.as_view(), name='company_detail'),
]