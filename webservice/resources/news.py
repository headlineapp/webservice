from django.db.models import Sum, F
from webservice.models import *
from .channel import ChannelResource

from tastypie import fields
from tastypie.serializers import Serializer
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS

import datetime


class NewsResource(ModelResource):
    class Meta:
        queryset = News.objects.all()
        resource_name = 'news/all'
        serializer = Serializer(formats=['json'])

    def get_object_list(self, request):
        return super(LatestNewsResource, self).\
            get_object_list(request).\
            exclude(url_title__isnull=True,
                    url_title='',
                    url_image__isnull=True,
                    url_image='',
                    url_description__isnull=True,
                    url_description='')


class LatestNewsResource(ModelResource):
    channel = fields.ForeignKey(ChannelResource, 'channel', full=True)

    class Meta:
        queryset = News.objects.all()
        resource_name = 'news/latest'
        serializer = Serializer(formats=['json'])
        filtering = {
            'channel' : ALL_WITH_RELATIONS,
            'pk' : ALL_WITH_RELATIONS,
        }

    def get_object_list(self, request):
        uuid = request.GET.get('uuid')
        channel_id = request.GET.get('channel_id')
        if uuid:
            channel = Channel.objects.filter(subscriber__uuid=uuid)
            return super(LatestNewsResource, self).\
                get_object_list(request).\
                exclude(channel__in=channel,
                        url_title__isnull=True,
                        url_title='',
                        url_image__isnull=True,
                        url_image='',
                        url_description__isnull=True,
                        url_description='')
        elif channel_id:
            channel_id = request.GET.get('channel_id')
            return super(LatestNewsResource, self).get_object_list(request).filter(channel__pk=channel_id)
        else:
            return super(LatestNewsResource, self).get_object_list(request).all()


class TrendingNewsResource(ModelResource):
    channel = fields.ForeignKey(ChannelResource, 'channel', full=True)

    class Meta:
        queryset = News.objects.all()
        resource_name = 'news/trending'
        serializer = Serializer(formats=['json'])
        filtering = {
            'channel' : ALL_WITH_RELATIONS,
            'pk' : ALL_WITH_RELATIONS,
        }

    def get_object_list(self, request):
        yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
        return super(TrendingNewsResource, self).\
            get_object_list(request).\
            exclude(twitter_date_posted__gte=yesterday,
                    url_title__isnull=True,
                    url_title='',
                    url_image__isnull=True,
                    url_image='',
                    url_description__isnull=True,
                    url_description='').\
            annotate(score=Sum(F('twitter_retweet_count')+F('twitter_favorite_count'))).\
            order_by('-score')

