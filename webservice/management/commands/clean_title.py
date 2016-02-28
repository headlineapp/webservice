from django.core.management.base import BaseCommand
from webservice.models import News


class Command(BaseCommand):
    def handle(self, *args, **options):
        all_news = News.objects.filter(url_title__isnull=False)
        for news in all_news:
            url_title = news.url_title
            url_title = url_title.replace(' - %s', news.channel.name)
            url_title = url_title.replace(' | %s', news.channel.name)
            news.url_title = url_title
            news.save()