# -*- coding: utf-8 -*-

import re
import json
import requests

from PIL import Image
from io import BytesIO
from django.db.models import Q
from webservice.twitter import *
from dateutil import parser
from bs4 import BeautifulSoup as bsoup
from webservice.models import Channel, News
from headline.settings import \
    TWITTER_ACCESS_TOKEN, \
    TWITTER_CONSUMER_SECRET, \
    TWITTER_CONSUMER_KEY, \
    TWITTER_TOKEN_SECRET


def pull_latest_status(count=200):
    channels = Channel.objects.all()
    for channel in channels:
        screen_name = channel.twitter_screen_name

        # print '\nFetching data from @%s...' % screen_name

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
            # print status
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

            # print '\n\nstatus id : %s' % status_id
            # print 'text : %s' % text
            # print 'url : %s' % url
            # print 'url image : %s' % url_image
            # print 'created_at : %s' % created_at
            # print 'json : %s' % json.dumps(status)

            if 'RT' not in text \
                    and "@" not in text \
                    and '#' not in text \
                    and url is not None \
                    and url is not '' \
                    and is_quote_status is False \
                    and in_reply_to_status_id is None \
                    and is_retweeted is False:
                # print '\n\nstatus id : %s' % status_id
                # print 'text : %s' % text
                # print 'url : %s' % url
                # print 'url image : %s' % url_image
                # print 'created_at : %s' % created_at
                # print 'json : %s' % json.dumps(status)

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
                        # print response.url
                        news.url = response.url
                        news.save()
                        number_of_new_news += 1

                else:
                    news.twitter_favorite_count = favorite_count
                    news.twitter_retweet_count = retweet_count
                    news.twitter_date_posted = parser.parse(created_at)
                    news.save()
                    number_of_updated_news += 1

            # else:
                # print 'failed saving url with status id %s' % status_id

        last_news = News.objects.filter(channel=channel).reverse().last()
        if last_news:
            Channel.objects.filter(pk=channel.pk).update(twitter_since_id=last_news.twitter_id,
                                                         twitter_last_date=last_news.twitter_date_posted)

        # print '%d saved & %d updated' % (number_of_new_news, number_of_updated_news)

    # print '\nTotal %d news from twitter' % News.objects.count()

    # total = News.objects.filter(url_title__isnull=False, url_description__isnull=False).count()
    # print '\nDone. Currently we have %d news available to read.\n' % total

        previous_latest_news = channel.latest_news.all()
        for latest_news in previous_latest_news:
            channel.latest_news.remove(latest_news)
            channel.save()

        latest_news = News.objects.filter(channel=channel)[:2]
        latest_news = list(latest_news)
        channel.latest_news.add(*latest_news)
        channel.save()


def pull_title_and_images():
    filter_query = Q(url_title=None) | Q(url_title='') | Q(url_image=None) | Q(url_image='')
    url_without_title = News.objects.filter(filter_query).values_list('url', flat=True)
    # print '\nGetting %d news title & description...' % len(url_without_title)

    for url in url_without_title:
        # print url
        response = requests.get(url)
        if response:
            soup = bsoup(response.text, "html.parser")

            url_title = None
            if soup.title:
                url_title = soup.title.string
            # print url_title

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
            # print url_description

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
            # print url_image
            # print soup
            # print ''

            # Remove duplicate news
            for news in News.objects.values_list('url', flat=True).distinct():
                News.objects.filter(pk__in=News.objects.filter(url=url).values_list('id', flat=True)[1:]).delete()

            news = News.objects.get(url=url)
            if url_title:
                url_title = url_title.replace(' - %s' % news.channel.name, '')
                url_title = url_title.replace(' | %s' % news.channel.name, '')
                news.url_title = url_title
            news.url_description = url_description
            news.save()

            News.objects.filter(url=url, url_image__isnull=True).update(url_image=url_image)

            # print News.objects.count()


def get_image_width(url):
    try:
        data = requests.get(url).content
        im = Image.open(BytesIO(data))
        return im.size[0]
    except requests.exceptions.RequestException as e:
        return 0


def get_biggest_images(images):
    biggest_photo_url = None
    biggest_photo_width = 0
    for image in images:
        if 'src' in image:
            width = get_image_width(image['src'])
            if width > biggest_photo_width:
                biggest_photo_width = width
                biggest_photo_url = image['src']
    return biggest_photo_url
