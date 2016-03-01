from django.test import TestCase
from webservice.models import Channel
from webservice.twitter.pull_data import pull_latest_status, pull_title_and_images


class ChannelTest(TestCase):
    def setUp(self):
        Channel(name='AP', twitter_screen_name='AP').save()
        pass

    def test_load_channel(self):
        pull_latest_status(count=10)
        pull_title_and_images()

    def tearDown(self):
        pass

