import requests

from django_cron import CronJobBase, Schedule
from django.db.models import Q
from webservice.twitter import *
from webservice.util import get_biggest_images
from dateutil import parser
from bs4 import BeautifulSoup as bsoup
from webservice.models import Channel, News, Category
from headline.settings import \
    TWITTER_ACCESS_TOKEN, \
    TWITTER_CONSUMER_SECRET, \
    TWITTER_CONSUMER_KEY, \
    TWITTER_TOKEN_SECRET


class TwitterCronJob(CronJobBase):

    RUN_EVERY_MINUTES = 10
    RETRY_AFTER_FAILURE_MINS = 5
    schedule = Schedule(run_every_mins=RUN_EVERY_MINUTES)
    code = 'webservice.cron.twitter_cron_job'

    def do(self):
        self.update_channel()
        self.update_category()
        self.update_news()

    def update_channel(self):
        api = Twitter(auth=OAuth(TWITTER_ACCESS_TOKEN,
                                 TWITTER_TOKEN_SECRET,
                                 TWITTER_CONSUMER_KEY,
                                 TWITTER_CONSUMER_SECRET))
        twitter_screen_names = Channel.objects.all().values_list('twitter_screen_name', flat=True)
        twitter_screen_names = ','.join(twitter_screen_names)
        channel_data = api.users.lookup(screen_name=twitter_screen_names)
        for data in channel_data:
            screen_name = data.get('screen_name')
            profile_image_url = data.get('profile_image_url_https')
            Channel.objects.\
                filter(twitter_screen_name=screen_name).\
                update(profile_image_url=profile_image_url)

    def update_category(self):
        categories = Category.objects.all()
        for category in categories:
            channels = Channel.objects.filter(category=category)
            number_of_channels = channels.count()
            category_icon_url = channels.first().profile_image_url
            category.number_of_channel = number_of_channels
            category.category_icon_url = category_icon_url
            category.save()

    def update_news(self):
        self.pull_latest_status()
        self.pull_title_and_images()

    def pull_latest_status(self, count=200):
        self.remove_duplicate_news()
        channels = Channel.objects.all()
        for channel in channels:
            screen_name = channel.twitter_screen_name

            api = Twitter(auth=OAuth(TWITTER_ACCESS_TOKEN,
                                     TWITTER_TOKEN_SECRET,
                                     TWITTER_CONSUMER_KEY,
                                     TWITTER_CONSUMER_SECRET))

            if channel.twitter_since_id:
                statuses = api.statuses.user_timeline(screen_name=screen_name,
                                                      count=count,
                                                      since_id=channel.twitter_since_id)
            else:
                statuses = api.statuses.user_timeline(screen_name=screen_name, count=count, trim_user=True)

            number_of_new_news = 0
            number_of_updated_news = 0
            for status in statuses:
                status_id = status.get('id')
                text = status.get('text')
                text = re.sub(r"(?:\@|https?\://)\S+", "", text)

                url = None
                entities = status.get('entities')
                if 'urls' in entities:
                    if len(entities.get('urls')) > 0:
                        url = entities.get('urls')[0].get('expanded_url')

                url_image = None
                if 'media' in entities:
                    if len(entities.get('media')) > 0:
                        url_image = entities.get('media')[0].get('media_url_https')

                favorite_count = status.get('favorite_count')
                retweet_count = status.get('retweet_count')
                created_at = status.get('created_at')
                is_quote_status = status.get('is_quote_status')
                in_reply_to_status_id = status.get('in_reply_to_status_id')
                is_retweeted = status.get('retweeted')

                if 'RT' not in text \
                        and "@" not in text \
                        and '#' not in text \
                        and url is not None \
                        and url is not '' \
                        and is_quote_status is False \
                        and in_reply_to_status_id is None \
                        and is_retweeted is False:

                    News.objects.filter(pk__in=News.objects.filter(url=url).values_list('id', flat=True)[1:]).delete()
                    News.objects.filter(pk__in=News.objects.filter(twitter_text=text).values_list('id', flat=True)[1:]).delete()

                    news, created = News.objects.get_or_create(url=url)
                    if created:
                        news.channel = channel
                        news.url_image = url_image
                        news.twitter_id = status_id
                        news.twitter_text = text
                        news.twitter_favorite_count = favorite_count
                        news.twitter_retweet_count = retweet_count
                        news.twitter_date_posted = parser.parse(created_at)

                        session = requests.Session()
                        response = session.head(url, allow_redirects=True)
                        if response.url:
                            news.url = response.url
                            number_of_new_news += 1

                        news.save()

                    else:
                        news.twitter_favorite_count = favorite_count
                        news.twitter_retweet_count = retweet_count
                        news.twitter_date_posted = parser.parse(created_at)
                        news.save()
                        number_of_updated_news += 1

            last_news = News.objects.filter(channel=channel).reverse().last()
            if last_news:
                channel.twitter_since_id = last_news.twitter_id
                channel.twitter_last_date = last_news.twitter_date_posted

            channel.save()

        self.remove_duplicate_news()

    def pull_title_and_images(self):
        filter_query = Q(url_title=None) | Q(url_title='') | Q(url_image=None) | Q(url_image='')
        url_without_title = News.objects.filter(filter_query).values_list('url', flat=True)

        for url in url_without_title:
            response = requests.get(url)
            if response:
                soup = bsoup(response.text, "html.parser")

                url_title = None
                if soup.title:
                    url_title = soup.title.string

                url_description = None
                twitter_description = soup.find('meta', attrs={'property': 'twitter:description', 'content': True})
                og_description = soup.find('meta', attrs={'property': 'og:description', 'content': True})
                meta_description = soup.find('meta', attrs={'name': 'description', 'content': True})
                if twitter_description:
                    url_description = twitter_description['content']
                elif og_description:
                    url_description = og_description['content']
                elif meta_description:
                    url_description = meta_description['content']

                url_image = None
                twitter_image = soup.find('meta', attrs={'property': 'twitter:image:src', 'content': True})
                og_image = soup.find('meta', attrs={'property': 'og:image', 'content': True})
                if twitter_image:
                    url_image = twitter_image['content']
                elif og_image:
                    url_image = og_image['content']
                else:
                    images = soup.find_all('img')
                    url_image = get_biggest_images(images)

                news_is_exist = News.objects.filter(url=url).exists()
                if news_is_exist:
                    news = News.objects.get(url=url)
                    if url_title and url_description:
                        if news.channel:
                            url_title = url_title.replace(' - %s' % news.channel.name, '')
                            url_title = url_title.replace(' | %s' % news.channel.name, '')
                        news.url_title = url_title
                        news.url_description = url_description
                        news.save()
                        News.objects.filter(url=url, url_image__isnull=True).update(url_image=url_image)
                    else:
                        news.delete()

    def remove_duplicate_news(self):
        for url in News.objects.values_list('url', flat=True).distinct():
            News.objects.filter(pk__in=News.objects.filter(url=url).values_list('id', flat=True)[1:]).delete()
        for twitter_text in News.objects.values_list('twitter_text', flat=True).distinct():
            News.objects.filter(pk__in=News.objects.filter(twitter_text=twitter_text).values_list('id', flat=True)[1:]).delete()


