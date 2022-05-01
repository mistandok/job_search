from django.contrib import admin
from django.urls import path

from apps.jobsearch.views import (
    StartPageView, ListVacancyView, DetailVacancyView, DetailCompanyView,
    ListSpecialtyVacancyView, ApplicationView, MyCompanyCreateView, MyCompanyLetsStartView,
    MyCompanyUpdateView, MyCompanyVacanciesLetsStartView, MyCompanyVacanciesCreateView,
    MyCompanyVacanciesListView, MyCompanyVacanciesUpdateView, MyCompanyVacanciesDeleteView
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

urlpatterns += [
    path('mycompany/create', MyCompanyCreateView.as_view(), name='my_company_create'),
    path('mycompany/letsstart', MyCompanyLetsStartView.as_view(), name='my_company_lets_start'),
    path('mycompany/', MyCompanyUpdateView.as_view(), name='my_company_edit'),
]

urlpatterns += [
    path('mycompany/vacancies/letstart', MyCompanyVacanciesLetsStartView.as_view(), name='my_company_vacancies_lets_start'),
    path('mycompany/vacancies/create', MyCompanyVacanciesCreateView.as_view(), name='my_company_vacancies_create'),
    path('mycompany/vacancies/', MyCompanyVacanciesListView.as_view(), name='my_company_vacancies_list'),
    path('mycompany/vacancies/<int:pk>', MyCompanyVacanciesUpdateView.as_view(), name='my_company_vacancies_update'),
    path('mycompany/vacancies/<int:pk>/delete', MyCompanyVacanciesDeleteView.as_view(), name='my_company_vacancies_delete'),
]
