"""conf URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from apps.jobsearch.views import (
    StartPageView, ListVacancyView, DetailVacancyView, DetailCompanyView, ListSpecialtyVacancyView,
    handler404_view, handler500_view
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', StartPageView.as_view(), name='start_page'),
    path('vacancies/', ListVacancyView.as_view(), name='all_vacancies'),
    path('vacancies/cat/<str:specialty>', ListSpecialtyVacancyView.as_view(), name='vacancies_for_specialty'),
    path('vacancies/<int:pk>', DetailVacancyView.as_view(), name='vacancy_detail'),
    path('companies/<int:pk>', DetailCompanyView.as_view(), name='company_detail'),
]

handler404 = handler404_view
handler500 = handler500_view
