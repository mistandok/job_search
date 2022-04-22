from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import CheckConstraint, Q, F


class Company(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    logo = models.URLField(default='https://place-hold.it/100x60')
    description = models.TextField()
    employee_count = models.IntegerField()


class Specialty (models.Model):
    class SpecialtyChoises(models.TextChoices):
        FRONTEND = 'frontend', 'Фронтенд'
        BACKEND = 'backend', 'Бэкенд'
        GAMEDEV = 'gamedev', 'Геймдев'
        DEVOPS = 'devops', 'Девопс'
        DESIGN = 'design', 'Дизайн'
        PRODUCTS = 'products', 'Продукты'
        MANAGEMENT = 'management', 'Менеджмент'
        TESTING = 'testing', 'Тестирование'

    code = models.CharField(max_length=15, unique=True, choices=SpecialtyChoises.choices)
    title = models.CharField(max_length=100)
    picture = models.URLField(default='https://place-hold.it/100x60')


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
