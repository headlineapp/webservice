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
        filtering = {
            'url_title': ALL,
        }

    def get_object_list(self, request):
        return super(NewsResource, self).\
            get_object_list(request).\
            exclude(url_title__isnull=True)


class LatestNewsResource(ModelResource):
    channel = fields.ForeignKey(ChannelResource, 'channel', full=True)

    class Meta:
        queryset = News.objects.all()
        resource_name = 'news/latest'
        serializer = Serializer(formats=['json'])
        filtering = {
            'channel': ALL_WITH_RELATIONS,
            'pk': ALL_WITH_RELATIONS,
        }

    def get_object_list(self, request):
        IDFA = request.GET.get('IDFA')
        channel_id = request.GET.get('channel_id')
        if IDFA:
            subscriber = Subscriber.objects.get(IDFA=IDFA)
            channels = subscriber.channel
            return super(LatestNewsResource, self).\
                get_object_list(request).\
                exclude(channel__in=channels,
                        url_title__isnull=True)
        elif channel_id:
            channel_id = request.GET.get('channel_id')
            return super(LatestNewsResource, self).\
                get_object_list(request).\
                filter(channel__pk=channel_id,
                       url_title__isnull=False)
        else:
            return super(LatestNewsResource, self).\
                get_object_list(request).\
                exclude(url_title__isnull=True)


class TrendingNewsResource(ModelResource):
    channel = fields.ForeignKey(ChannelResource, 'channel', full=True)

    class Meta:
        queryset = News.objects.all()
        resource_name = 'news/trending'
        serializer = Serializer(formats=['json'])
        filtering = {
            'channel': ALL_WITH_RELATIONS,
            'pk': ALL_WITH_RELATIONS,
        }

    def get_object_list(self, request):
        yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
        return super(TrendingNewsResource, self).\
            get_object_list(request).\
            filter(twitter_date_posted__gte=yesterday).\
            exclude(url_title__isnull=True).\
            annotate(score=Sum(F('twitter_retweet_count')+F('twitter_favorite_count'))).\
            order_by('-score')

