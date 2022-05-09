from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView

from ..forms import MyCompanyForm
from ..helpers.navigation import (
    redirect_for_user, CompanyExistForUserChecker
)
from ..models import Company


@method_decorator(login_required(login_url='/login/'), name='dispatch')
@method_decorator(
    redirect_for_user(
        is_object_should_exist=True,
        redirect_to='my_company_edit',
        object_exists_checker=CompanyExistForUserChecker()
    ),
    name='dispatch'
)
class MyCompanyLetsStartView(TemplateView):
    login_url = 'login'
    template_name = 'jobsearch/company/company_create.html'


@method_decorator(login_required(login_url='/login/'), name='dispatch')
@method_decorator(
    redirect_for_user(
        is_object_should_exist=True,
        redirect_to='my_company_edit',
        object_exists_checker=CompanyExistForUserChecker()
    ),
    name='dispatch'
)
class MyCompanyCreateView(CreateView):
    login_url = 'login'
    template_name = 'jobsearch/company/company_edit.html'

    model = Company
    form_class = MyCompanyForm

    def get_success_url(self):
        return reverse('my_company_edit')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(MyCompanyCreateView, self).form_valid(form)


@method_decorator(login_required(login_url='/login/'), name='dispatch')
@method_decorator(
    redirect_for_user(
        is_object_should_exist=False,
        redirect_to='my_company_lets_start',
        object_exists_checker=CompanyExistForUserChecker()
    ),
    name='dispatch'
)
class MyCompanyUpdateView(SuccessMessageMixin, UpdateView):
    login_url = 'login'
    template_name = 'jobsearch/company/company_edit.html'
    success_message = 'Компания обновлена'

    model = Company
    form_class = MyCompanyForm

    def get_object(self, queryset=None):
        return self.model.objects.get(owner=self.request.user)

    def get_success_url(self):
        return reverse('my_company_edit')
