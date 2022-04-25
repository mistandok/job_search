from django.contrib import admin

from .models import Company, Specialty, Vacancy


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'location',
        'logo',
        'description',
        'employee_count',
    )
    search_fields = ('name',)


@admin.register(Specialty)
class SpecialtyAdmin(admin.ModelAdmin):
    list_display = ('id', 'code', 'title', 'picture')


@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'specialty',
        'company',
        'skills',
        'description',
        'salary_min',
        'salary_max',
        'published_at',
    )
    list_filter = ('specialty', 'company', 'published_at')
