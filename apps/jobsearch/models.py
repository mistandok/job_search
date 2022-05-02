from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import CheckConstraint, Q, F
from phonenumber_field.modelfields import PhoneNumberField


class Company(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    logo = models.ImageField(upload_to=settings.MEDIA_COMPANY_IMAGE_DIR)
    description = models.TextField()
    employee_count = models.IntegerField()
    owner = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='company', null=True)


class Specialty (models.Model):
    code = models.CharField(max_length=15, unique=True)
    title = models.CharField(max_length=100)
    picture = models.ImageField(upload_to=settings.MEDIA_SPECIALITY_IMAGE_DIR)

    class Meta:
        indexes = [
            models.Index(fields=['code']),
        ]

    def __str__(self):
        return f'{self.title}'


class Vacancy(models.Model):
    title = models.CharField(max_length=100)
    specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE, related_name='vacancies')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='vacancies')
    skills = models.TextField()
    description = models.TextField()
    salary_min = models.DecimalField(max_digits=15, decimal_places=2)
    salary_max = models.DecimalField(max_digits=15, decimal_places=2)
    published_at = models.DateField()

    class Meta:
        constraints = [
            CheckConstraint(check=Q(salary_max__gte=F('salary_min')), name='check_salary')
        ]

    def clean(self):
        super().clean()
        if self.salary_min > self.salary_max:
            raise ValidationError({'salary_max': 'Максимальная зарплата не может быть меньше, чем минимальная.'})


class Application(models.Model):
    written_username = models.CharField(max_length=100)
    written_phone = PhoneNumberField()
    written_cover_letter = models.TextField()
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE, related_name='applications')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='applications')

    class Meta:
        unique_together = ('vacancy', 'user',)


class Resume(models.Model):
    SEARCH_STATES = (
        ('SEARCH_JOB', 'Ищу работу'),
        ('DONT_SEARCH_JOB', 'Не ищу работу'),
        ('OPREN_TO_OFFERS', 'Открыт к предложениям')
    )

    QUALIFICATIONS = (
        ('JUNIOR', 'Младший (Junior)'),
        ('MIDDLE', 'Средний (Middle)'),
        ('SENIOR', 'Старший (Senior)'),
    )

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    search_state = models.CharField(max_length=50, choices=SEARCH_STATES)
    qualification = models.CharField(max_length=50, choices=QUALIFICATIONS)
    expected_salary = models.DecimalField(max_digits=15, decimal_places=2)
    specialty = models.ForeignKey(Specialty, on_delete=models.SET_NULL, related_name='resumes', null=True)
    education = models.TextField()
    experience = models.TextField()
    link_to_portfolio = models.URLField()
    owner = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='resumes')
