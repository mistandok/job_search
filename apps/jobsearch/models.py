from django.db import models


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

    code = models.CharField(max_length=15, choices=SpecialtyChoises.choices, primary_key=True)
    title = models.CharField(max_length=100)
    picture = models.URLField(default='https://place-hold.it/100x60')


class Vacancy(models.Model):
    title = models.CharField(max_length=100)
    specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE, related_name='vacancies', to_field='code')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='vacancies')
    skills = models.TextField()
    description = models.TextField()
    salary_min = models.IntegerField()
    salary_max = models.IntegerField()
    published_at = models.DateField()

