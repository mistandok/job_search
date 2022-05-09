from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView

from ..forms import MyResumeForm
from ..helpers.navigation import (
    redirect_for_user, ResumeExistForUserChecker
)
from ..models import Resume


@method_decorator(login_required(login_url='/login/'), name='dispatch')
@method_decorator(
    redirect_for_user(
        is_object_should_exist=True,
        redirect_to='my_resume_edit',
        object_exists_checker=ResumeExistForUserChecker()
    ),
    name='dispatch'
)
class MyResumeLetsStartView(TemplateView):
    login_url = 'login'
    template_name = 'jobsearch/resume/resume_letsstart.html'


@method_decorator(login_required(login_url='/login/'), name='dispatch')
@method_decorator(
    redirect_for_user(
        is_object_should_exist=True,
        redirect_to='my_resume_edit',
        object_exists_checker=ResumeExistForUserChecker()
    ),
    name='dispatch'
)
class MyResumeCreateView(CreateView):
    login_url = 'login'
    template_name = 'jobsearch/resume/resume_edit.html'

    model = Resume
    form_class = MyResumeForm

    def get_success_url(self):
        return reverse('my_resume_edit')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(MyResumeCreateView, self).form_valid(form)


@method_decorator(login_required(login_url='/login/'), name='dispatch')
@method_decorator(
    redirect_for_user(
        is_object_should_exist=False,
        redirect_to='my_resume_lets_start',
        object_exists_checker=ResumeExistForUserChecker()
    ),
    name='dispatch'
)
class MyResumeUpdateView(SuccessMessageMixin, UpdateView):
    login_url = 'login'
    template_name = 'jobsearch/resume/resume_edit.html'
    success_message = 'Резюме обновлено'

    model = Resume
    form_class = MyResumeForm

    def get_object(self, queryset=None):
        return self.model.objects.get(owner=self.request.user)

    def get_success_url(self):
        return reverse('my_resume_edit')
    