from django.core.management.base import BaseCommand
from webservice.models import News


class Command(BaseCommand):
    def handle(self, *args, **options):
        for row in News.objects.all():
            if News.objects.filter(url=row.url).count() > 1:
                row.delete()
        print News.objects.count()