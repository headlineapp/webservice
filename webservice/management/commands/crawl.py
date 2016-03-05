from django.core.management.base import BaseCommand
from webservice.twitter.pull_data import \
    pull_latest_status, \
    pull_title_and_images, \
    remove_duplicate_news, \
    update_channel_latest_news


class Command(BaseCommand):
    def handle(self, *args, **options):
        pull_latest_status()
        remove_duplicate_news()
        pull_title_and_images()
        update_channel_latest_news()