from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit
from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _

from .models import Application, Company, Vacancy


class ApplicationForm(forms.ModelForm):
    written_username = forms.CharField(
        label=_('Вас зовут'),
    )

    written_phone = forms.RegexField(
        label=_('Ваш телефон'),
        regex=r'^\+?1?\d{9,15}$',
        error_messages={'invalid': "Телефон должен соответствовать следующему формату: '+999999999'. Не более 15 символов."}
    )

    written_cover_letter = forms.CharField(
        label=_('Сопроводительное письмо'),
        widget=forms.Textarea()
    )

    class Meta:
        model = Application
        fields = ['written_username', 'written_phone', 'written_cover_letter']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.vacancy = kwargs.pop('vacancy', None)

        super(ApplicationForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'post'

        self.helper.layout = Layout(
            Fieldset(
                '<p class="h5 mt-3 font-weight-normal">Отозваться на вакансию</p>',
            ),
            Fieldset(
                '',
                'written_username',
                'written_phone',
                'written_cover_letter',
            ),
            ButtonHolder(Submit('submit', 'Отправить отклик'))
        )

    def clean(self):
        if not self.user or not self.user.is_authenticated:
            raise forms.ValidationError(_('Отправить отклик может только авторизованный пользователь.'))
        if self.vacancy and self.user:
            try:
                Application.objects.get(user=self.user, vacancy=self.vacancy)
                raise forms.ValidationError(_('Вы уже отправляли отклик на эту вакансию!'))
            except ObjectDoesNotExist:
                pass
        return self.cleaned_data


class MyCompanyForm(forms.ModelForm):
    name = forms.CharField(
        label=_('Название компании'),
        max_length=100,
    )

    employee_count = forms.IntegerField(
        label=_('Количество человек в компании'),
    )

    location = forms.CharField(
        label=_('География'),
        max_length=100,
    )

    logo = forms.ImageField(
        label=_('Логотип'),
        label_suffix=_('Загрузить')
    )

    description = forms.CharField(
        label=_('Информация о компании'),
        widget=forms.Textarea()
    )

    class Meta:
        model = Company
        fields = ['name', 'employee_count', 'location', 'logo', 'description']

    def __init__(self, *args, **kwargs):
        super(MyCompanyForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'post'

        self.helper.layout = Layout(
            Fieldset(
                '',
                'name',
                'employee_count',
                'location',
                'logo',
                'description'
            ),
            ButtonHolder(Submit('submit', 'Сохранить'))
        )


class MyVacancyForm(forms.ModelForm):
    title = forms.CharField(
        label=_('Название вакансии'),
        max_length=100,
    )

    # specialty = forms.Fo(
    #     label=_('Количество человек в компании'),
    # )
    #
    # location = forms.CharField(
    #     label=_('География'),
    #     max_length=100,
    # )
    #
    # logo = forms.ImageField(
    #     label=_('Логотип'),
    #     label_suffix=_('Загрузить')
    # )
    #
    # description = forms.CharField(
    #     label=_('Информация о компании'),
    #     widget=forms.Textarea()
    # )

    class Meta:
        model = Vacancy
        fields = ['title']

    def __init__(self, *args, **kwargs):
        super(MyVacancyForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'post'

        self.helper.layout = Layout(
            Fieldset(
                '',
                'title',
            ),
            ButtonHolder(Submit('submit', 'Сохранить'))
        )
