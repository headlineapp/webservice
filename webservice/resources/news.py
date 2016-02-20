from django.conf.urls import url
from django.db.models import Count

from webservice.models import *
from pagination import prepare_results

from channel import ChannelResource

from tastypie import fields
from tastypie.serializers import Serializer
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie.utils import trailing_slash


class NewsResource(ModelResource):
    channel = fields.ForeignKey(ChannelResource, 'channel')

    class Meta:
        queryset = News.objects.all()
        resource_name = 'news'
        serializer = Serializer(formats=['json'])
        filtering = {
            'channel' : ALL_WITH_RELATIONS,
            'pk' : ALL_WITH_RELATIONS,
        }

    def prepend_urls(self):
        url_latest_news = r"^(?P<resource_name>%s)/latest%s$" % (self._meta.resource_name, trailing_slash())
        url_trending_news = r"^(?P<resource_name>%s)/trending%s$" % (self._meta.resource_name, trailing_slash())
        return [
            url(url_latest_news, self.wrap_view('get_latest_news'), name="api_get_latest_news"),
            url(url_trending_news, self.wrap_view('get_trending_news'), name="api_get_trending_news"),
        ]

    def get_latest_news(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        uuid = request.GET.get('uuid')
        channel = Channel.objects.filter(subscriber__uuid=uuid)
        news = News.objects.filter(channel__in=channel)
        results = prepare_results(self, request, news)
        return self.create_response(request, results)

    def get_trending_news(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        news = News.objects.filter().annotate(num_submissions=Count('channel__subscriber')).order_by('-num_submissions')
        results = prepare_results(self, request, news)
        return self.create_response(request, results)


