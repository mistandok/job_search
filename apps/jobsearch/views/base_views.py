from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import FormMixin

from ..forms import ApplicationForm, SearchForm
from ..models import Vacancy, Company, Specialty
from ..services.api import get_vacancies_by_search_filter


class StartPageView(TemplateView):
    template_name = 'jobsearch/index.html'

    def get_context_data(self, **kwargs):
        context = super(StartPageView, self).get_context_data(**kwargs)
        context['specialties'] = Specialty.objects.annotate(count_vacancies=Count('vacancies')).all()
        context['companies'] = Company.objects.annotate(count_vacancies=Count('vacancies')).all()
        context['search_examples'] = ['Python', 'Flask', 'Django', 'Парсинг', 'ML']
        return context


class ListVacancyView(ListView):
    model = Vacancy
    template_name = 'jobsearch/vacancy/vacancies.html'

    def get_queryset(self):
        return super().get_queryset().select_related()


class SearchListVacancyView(FormMixin, ListView):
    template_name = 'jobsearch/vacancy/search_vacancies.html'
    form_class = SearchForm
    model = Vacancy

    def get_queryset(self):
        get_request = self.request.GET
        vacancies = get_vacancies_by_search_filter(get_request.get('search_filter', ''))
        return vacancies

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        get_request = self.request.GET
        kwargs['search_filter'] = get_request.get('search_filter', '')
        return kwargs


class ListSpecialtyVacancyView(ListView):
    model = Vacancy
    template_name = 'jobsearch/vacancy/vacancies.html'

    def get_queryset(self):
        return super().get_queryset().filter(specialty__code=self.kwargs.get('specialty')).select_related()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ListSpecialtyVacancyView, self).get_context_data(**kwargs)
        context['title'] = get_object_or_404(Specialty, code=self.kwargs.get('specialty')).title
        return context


class ApplicationView(TemplateView):
    template_name = 'jobsearch/vacancy/application_sended.html'


class DetailVacancyView(FormMixin, DetailView):
    model = Vacancy
    template_name = 'jobsearch/vacancy/vacancy.html'
    form_class = ApplicationForm

    def get_queryset(self):
        return super().get_queryset().select_related()

    def get_success_url(self):
        return reverse('application_sended', kwargs={'pk': self.object.id})

    def get_context_data(self, **kwargs):
        context = super(DetailVacancyView, self).get_context_data(**kwargs)
        context['form'] = kwargs.get('form', ApplicationForm())
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['vacancy'] = self.get_object()
        return kwargs

    def form_valid(self, form):
        application = form.save(commit=False)
        application.user = self.request.user
        application.vacancy = self.get_object()
        application.save()
        return super(DetailVacancyView, self).form_valid(form)


class DetailCompanyView(DetailView):
    model = Company
    template_name = 'jobsearch/company/company.html'

    def get_queryset(self):
        return super().get_queryset().annotate(count_vacancies=Count('vacancies'))

    def get_context_data(self, **kwargs):
        context = super(DetailCompanyView, self).get_context_data(**kwargs)
        context['vacancy_list'] = self.get_object().vacancies.all()
        return context
