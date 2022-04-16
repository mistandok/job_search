from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView

from .models import Vacancy, Company, Specialty


class StartPageView(TemplateView):
    template_name = 'jobsearch/index.html'

    def get_context_data(self, **kwargs):
        context = super(StartPageView, self).get_context_data(**kwargs)
        context['specialties'] = Specialty.objects.all()
        context['companies'] = Company.objects.all()
        return context


class ListVacancyView(ListView):
    model = Vacancy
    template_name = 'jobsearch/vacancies.html'


class ListSpecialtyVacancyView(ListView):
    model = Vacancy
    template_name = 'jobsearch/vacancies.html'

    def get_queryset(self):
        return super().get_queryset().filter(specialty=self.kwargs.get('specialty'))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ListSpecialtyVacancyView, self).get_context_data(**kwargs)
        context['title'] = get_object_or_404(Specialty, pk=self.kwargs.get('specialty')).title
        return context


class DetailVacancyView(DetailView):
    model = Vacancy
    template_name = 'jobsearch/vacancy.html'
    queryset = Vacancy.objects.select_related()


class DetailCompanyView(DetailView):
    model = Company
    template_name = 'jobsearch/company.html'
    queryset = Company.objects.select_related()

    def get_context_data(self, **kwargs):
        context = super(DetailCompanyView, self).get_context_data(**kwargs)
        context['vacancy_list'] = Vacancy.objects.filter(company=self.get_object())
        return context


def handler404_view(request, *args, **kwargs):
    response = render(
        request,
        'tours/404.html',
        context={
        }
    )
    response.status_code = 404
    return response
