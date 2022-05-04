from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Count
from django.http import Http404
from django.urls import reverse
from django.utils.timezone import now
from django.views.generic import ListView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from ..forms import MyVacancyForm, MyVacancyDeleteForm
from ..helpers.navigation import (
    redirect_for_user, CompanyExistForUserChecker, VacancyExistForUserChecker, is_correct_company_for_user
)
from ..models import Vacancy, Company


class MyCompanyVacanciesLetsStartView(LoginRequiredMixin, TemplateView):
    login_url = 'login'
    template_name = 'jobsearch/vacancy/company_vacancy_letstart.html'

    @redirect_for_user(
        is_object_should_exist=False,
        redirect_to='my_company_lets_start',
        object_exists_for_user_checker=CompanyExistForUserChecker()
    )
    @redirect_for_user(
        is_object_should_exist=True,
        redirect_to='my_company_vacancies_list',
        object_exists_for_user_checker=VacancyExistForUserChecker()
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class MyCompanyVacanciesCreateView(LoginRequiredMixin, CreateView):
    login_url = 'login'
    template_name = 'jobsearch/vacancy/company_vacancy_edit.html'

    model = Vacancy
    form_class = MyVacancyForm

    @redirect_for_user(
        is_object_should_exist=False,
        redirect_to='my_company_edit',
        object_exists_for_user_checker=CompanyExistForUserChecker()
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('my_company_vacancies_list')

    def form_valid(self, form):
        form.instance.company = Company.objects.get(owner=self.request.user)
        form.instance.published_at = now().date()
        return super(MyCompanyVacanciesCreateView, self).form_valid(form)


class MyCompanyVacanciesUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    login_url = 'login'
    template_name = 'jobsearch/vacancy/company_vacancy_edit.html'
    success_message = 'Вакансия обновлена'

    model = Vacancy
    form_class = MyVacancyForm

    @redirect_for_user(
        is_object_should_exist=False,
        redirect_to='my_company_lets_start',
        object_exists_for_user_checker=CompanyExistForUserChecker()
    )
    @redirect_for_user(
        is_object_should_exist=False,
        redirect_to='my_company_vacancies_lets_start',
        object_exists_for_user_checker=VacancyExistForUserChecker()
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return super(MyCompanyVacanciesUpdateView, self).get_queryset().annotate(count_applications=Count('applications'))

    def get_object(self, queryset=None):
        vacancy = super(MyCompanyVacanciesUpdateView, self).get_object(queryset)
        if not is_correct_company_for_user(vacancy.company, self.request.user):
            raise Http404
        return vacancy

    def get_success_url(self):
        return reverse('my_company_vacancies_update', kwargs={'pk': self.get_object().pk})

    def get_context_data(self, **kwargs):
        context = super(MyCompanyVacanciesUpdateView, self).get_context_data(**kwargs)
        context['application_list'] = self.get_object().applications.all()
        return context


class MyCompanyVacanciesDeleteView(LoginRequiredMixin, DeleteView):
    login_url = 'login'
    template_name = 'jobsearch/vacancy/company_vacancy_delete.html'

    model = Vacancy
    form_class = MyVacancyDeleteForm

    def get_object(self, queryset=None):
        vacancy = super(MyCompanyVacanciesDeleteView, self).get_object(queryset)
        if not is_correct_company_for_user(vacancy.company, self.request.user):
            raise Http404
        return vacancy

    def get_success_url(self):
        return reverse('my_company_vacancies_list')


class MyCompanyVacanciesListView(LoginRequiredMixin, ListView):
    login_url = 'login'
    template_name = 'jobsearch/vacancy/company_vacancy_list.html'

    model = Vacancy

    @redirect_for_user(
        is_object_should_exist=False,
        redirect_to='my_company_edit',
        object_exists_for_user_checker=CompanyExistForUserChecker()
    )
    @redirect_for_user(
        is_object_should_exist=False,
        redirect_to='my_company_vacancies_lets_start',
        object_exists_for_user_checker=VacancyExistForUserChecker()
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return (super().get_queryset().
                annotate(count_applications=Count('applications')).
                filter(company__owner=self.request.user))
    