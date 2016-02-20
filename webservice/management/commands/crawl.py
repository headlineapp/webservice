from django.core.management.base import BaseCommand, CommandError
from webservice.twitter.pull_data import pull_latest_status, pull_title_and_images


class Command(BaseCommand):
    def handle(self, *args, **options):
        pull_latest_status()
        pull_title_and_images()
