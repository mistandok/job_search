from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import FormMixin, CreateView, UpdateView

from .forms import ApplicationForm, MyCompanyForm, MyVacancyForm
from .models import Vacancy, Company, Specialty
from .services.helpers import my_company_redirect_for_user, my_vacancy_redirect_for_user


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


class MyCompanyLetsStartView(LoginRequiredMixin, TemplateView):
    login_url = 'login'
    template_name = 'jobsearch/company/company-create.html'

    @my_company_redirect_for_user(is_company_should_exist=True, redirect_to='my_company_edit')
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class MyCompanyCreateView(LoginRequiredMixin, CreateView):
    login_url = 'login'
    template_name = 'jobsearch/company/company-edit.html'

    form_class = MyCompanyForm

    @my_company_redirect_for_user(is_company_should_exist=True, redirect_to='my_company_edit')
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('my_company_edit')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.save()
        return super(MyCompanyCreateView, self).form_valid(form)


class MyCompanyUpdateView(LoginRequiredMixin, UpdateView):
    login_url = 'login'
    template_name = 'jobsearch/company/company-edit.html'

    model = Company
    form_class = MyCompanyForm

    @my_company_redirect_for_user(is_company_should_exist=False, redirect_to='my_company_lets_start')
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return self.model.objects.get(owner=self.request.user)

    def get_success_url(self):
        return reverse('my_company_edit')


class MyCompanyVacanciesLetsStartView(LoginRequiredMixin, TemplateView):
    login_url = 'login'
    template_name = 'jobsearch/vacancy/vacancy-letstart.html'

    @my_company_redirect_for_user(is_company_should_exist=False, redirect_to='my_company_lets_start')
    @my_vacancy_redirect_for_user(is_vacancies_should_exist=True, redirect_to='my_company_vacancies_list')
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class MyCompanyVacanciesCreateView(LoginRequiredMixin, CreateView):
    login_url = 'login'
    template_name = 'jobsearch/vacancy/vacancy-edit.html'

    form_class = MyVacancyForm

    @my_company_redirect_for_user(is_company_should_exist=False, redirect_to='my_company_edit')
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('my_company_edit')

    def form_valid(self, form):
        return super(MyCompanyCreateView, self).form_valid(form)


class MyCompanyVacanciesListView(LoginRequiredMixin, ListView):
    login_url = 'login'
    template_name = 'jobsearch/vacancy/vacancy-list.html'

    model = Vacancy

    @my_company_redirect_for_user(is_company_should_exist=False, redirect_to='my_company_edit')
    @my_vacancy_redirect_for_user(is_vacancies_should_exist=False, redirect_to='my_company_vacancies_lets_start')
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return super().get_queryset().filter(company__owner=self.request.user)


def handler404_view(request, *args, **kwargs):
    response = render(
        request,
        'jobsearch/error/404.html',
        context={
            'information': 'Эта информация не представлена на сайте :('
        }
    )
    response.status_code = 404
    return response


def handler500_view(request, *args, **kwargs):
    response = render(
        request,
        'jobsearch/error/500.html',
        context={
            'information': 'Ой-ей, скоро мы это исправим!'
        }
    )
    response.status_code = 500
    return response
