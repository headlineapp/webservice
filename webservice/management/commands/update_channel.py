from django.core.management.base import BaseCommand
from webservice.cron import TwitterCronJob


class Command(BaseCommand):
    def handle(self, *args, **options):
        cron = TwitterCronJob()
        cron.update_channel()