from django.conf.urls import url
from django.db.models import Sum, F

from webservice.models import *

from .pagination import prepare_results
from .channel import ChannelResource

from tastypie import fields
from tastypie.serializers import Serializer
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie.utils import trailing_slash

import datetime


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
        channel = Channel.objects.filter(subscriber__uuid=uuid)
        return super(LatestNewsResource, self).get_object_list(request).filter(channel__in=channel)


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
            filter(twitter_date_posted__gte=yesterday).\
            annotate(score=Sum(F('twitter_retweet_count')+F('twitter_favorite_count'))).\
            order_by('-score')


