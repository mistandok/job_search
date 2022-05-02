from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView

from ..forms import MyResumeForm
from ..helpers.navigation import (
    redirect_for_user, ResumeExistForUserChecker
)
from ..models import Resume


class MyResumeLetsStartView(LoginRequiredMixin, TemplateView):
    login_url = 'login'
    template_name = 'jobsearch/resume/resume_letsstart.html'

    @redirect_for_user(
        is_object_should_exist=True,
        redirect_to='my_resume_edit',
        object_exists_for_user_checker=ResumeExistForUserChecker()
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class MyResumeCreateView(LoginRequiredMixin, CreateView):
    login_url = 'login'
    template_name = 'jobsearch/resume/resume_edit.html'

    model = Resume
    form_class = MyResumeForm

    @redirect_for_user(
        is_object_should_exist=True,
        redirect_to='my_resume_edit',
        object_exists_for_user_checker=ResumeExistForUserChecker()
    )
    def get(self, request, *args, **kwargs):
        return super(MyResumeCreateView, self).get(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('my_resume_edit')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(MyResumeCreateView, self).form_valid(form)


class MyResumeUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    login_url = 'login'
    template_name = 'jobsearch/resume/resume_edit.html'
    success_message = 'Резюме обновлено'

    model = Resume
    form_class = MyResumeForm

    @redirect_for_user(
        is_object_should_exist=False,
        redirect_to='my_resume_lets_start',
        object_exists_for_user_checker=ResumeExistForUserChecker()
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return self.model.objects.get(owner=self.request.user)

    def get_success_url(self):
        return reverse('my_resume_edit')
    