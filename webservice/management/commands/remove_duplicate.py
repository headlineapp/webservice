from django.core.management.base import BaseCommand
from webservice.models import News


class Command(BaseCommand):
    def handle(self, *args, **options):
        for url in News.objects.values_list('url', flat=True).distinct():
            News.objects.filter(pk__in=News.objects.filter(url=url).values_list('id', flat=True)[1:]).delete()
            print url
        for twitter_text in News.objects.values_list('twitter_text', flat=True).distinct():
            News.objects.filter(pk__in=News.objects.filter(twitter_text=twitter_text).values_list('id', flat=True)[1:]).delete()
            print url
        print News.objects.count()
