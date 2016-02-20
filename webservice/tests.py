from django.test import TestCase
from webservice.models import Channel
from webservice.twitter.pull_data import pull_latest_status, pull_title_and_images


class ChannelTest(TestCase):
    def setUp(self):
        Channel(name='AP', screen_name='AP', twitter_since_id='700366921741553664').save()
        pass

    def test_load_channel(self):
        pull_latest_status(count=2)
        pull_title_and_images()

    def tearDown(self):
        pass

