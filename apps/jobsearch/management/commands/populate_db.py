from django.core.management.base import BaseCommand
from apps.jobsearch.models import Vacancy, Company, Specialty
from data import jobs, companies, specialties


class Command(BaseCommand):
    args = None
    help = 'The command truncates and then fills database with data from data.py'

    def _truncate_db(self):
        Vacancy.objects.all().delete()
        Company.objects.all().delete()
        Specialty.objects.all().delete()

    def _populate_db(self):
        for company in companies:
            Company.objects.create(**company)

        for specialty in specialties:
            Specialty.objects.create(**specialty)

        for job in jobs:
            job['specialty'] = Specialty.objects.get(code=job['specialty'])
            job['company'] = Company.objects.get(id=job['company'])
            job['salary_max'] = job.pop('salary_to')
            job['salary_min'] = job.pop('salary_from')
            job['published_at'] = job.pop('posted')
            Vacancy.objects.create(**job)

    def handle(self, *args, **options):
        self._truncate_db()
        self._populate_db()
