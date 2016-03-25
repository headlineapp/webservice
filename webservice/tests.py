from django.test import TestCase
from webservice.models import Channel
from webservice.cron import TwitterCronJob


class ChannelTest(TestCase):
    def setUp(self):
        Channel(name='AP', twitter_screen_name='AP').save()
        pass

    def test_load_channel(self):
        cron = TwitterCronJob()
        cron.pull_latest_status(count=10)
        cron.remove_duplicate_news()
        cron.pull_title_and_images()

    def tearDown(self):
        pass

