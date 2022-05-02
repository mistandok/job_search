from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Button, BaseInput
from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from .models import Application, Company, Vacancy, Specialty, Resume


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

    specialty = forms.ModelChoiceField(
        label=_('Специализация'),
        queryset=Specialty.objects.all(),
        empty_label=None,
    )

    salary_min = forms.DecimalField(
        label=_('Зарплата от'),
        min_value=0,
        max_digits=15,
        decimal_places=2,
    )

    salary_max = forms.DecimalField(
        label=_('Зарплата до'),
        min_value=0,
        max_digits=15,
        decimal_places=2,
    )

    skills = forms.CharField(
        label=_('Требуемые навыки'),
        widget=forms.Textarea(),
    )

    description = forms.CharField(
        label=_('Описание вакансии'),
        widget=forms.Textarea(),
    )

    class Meta:
        model = Vacancy
        fields = ['title', 'specialty', 'salary_min', 'salary_max', 'skills', 'description']

    def __init__(self, *args, **kwargs):
        super(MyVacancyForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'post'

        self.helper.layout = Layout(
            Fieldset(
                '',
                'title',
                'specialty',
                'salary_min',
                'salary_max',
                'skills',
                'description',
            ),
            ButtonHolder(Submit('submit', 'Сохранить'))
        )


class MyVacancyDeleteForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(MyVacancyDeleteForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'post'

        self.helper.layout = Layout(
            Fieldset(
                f'Вы точно хотите удалить вакансию?',
            ),
            ButtonHolder(
                Submit('submit', 'Удалить', css_class='btn-danger'),
                Button('cancel', 'Не удалять', css_class='btn-primary', onclick="window.location.href = '{}';".format(reverse('my_company_vacancies_list')))
            )
        )


class SearchForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.search_filter = kwargs.pop('search_filter', '')

        super(SearchForm, self).__init__(self, *args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'get'

        self.helper.layout = Layout(
            Fieldset(
                'Найти вакансию',
                BaseInput(name='search_filter', value=self.search_filter),
            ),
            ButtonHolder(
                # BaseInput(name='search', value='Найти по ключевому слову'),
                Submit('submit', 'Найти', css_class='btn-primary'),
            )
        )


class MyResumeForm(forms.ModelForm):
    first_name = forms.CharField(
        label=_('Имя'),
        max_length=100,
    )

    last_name = forms.CharField(
        label=_('Фамилия'),
        max_length=100,
    )

    search_state = forms.ChoiceField(
        label=_('Готовность к работе'),
        choices=Resume.SEARCH_STATES,
    )

    expected_salary = forms.DecimalField(
        label=_('Ожидаемое вознаграждение'),
        min_value=0,
        max_digits=15,
        decimal_places=2,
    )

    specialty = forms.ModelChoiceField(
        label=_('Специализация'),
        queryset=Specialty.objects.all(),
        empty_label='Не указано',
    )

    qualification = forms.ChoiceField(
        label=_('Требуемые навыки'),
        choices=Resume.QUALIFICATIONS,
    )

    education = forms.CharField(
        label=_('Образование'),
        widget=forms.Textarea(),
    )

    experience = forms.CharField(
        label=_('Опыт работы'),
        widget=forms.Textarea(),
    )

    link_to_portfolio = forms.URLField(
        label=_('Ссылка на портфолио')
    )

    class Meta:
        model = Resume
        fields = [
            'first_name', 'last_name', 'search_state',
            'education', 'experience', 'link_to_portfolio',
            'specialty', 'expected_salary', 'qualification'
        ]

    def __init__(self, *args, **kwargs):
        super(MyResumeForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'post'

        self.helper.layout = Layout(
            Fieldset(
                '',
                'first_name',
                'last_name',
                'search_state',
                'expected_salary',
                'specialty',
                'qualification',
                'education',
                'experience',
                'link_to_portfolio',
            ),
            ButtonHolder(Submit('submit', 'Сохранить'))
        )
