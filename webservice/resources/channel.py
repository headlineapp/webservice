from django.conf.urls import url
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, InvalidPage
from webservice.models import *
from tastypie import fields
from tastypie.serializers import Serializer
from tastypie.paginator import Paginator as AutoPaginator
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie.utils import trailing_slash
from django.http import Http404
from .pagination import prepare_results


class ChannelResource(ModelResource):
    class Meta:
        queryset = Channel.objects.all()
        resource_name = 'channel'
        serializer = Serializer(formats=['json'])
        paginator_class = AutoPaginator
        filtering = {
            'name' : ALL,
        }


class SubscriptionResource(ModelResource):
    latest_news = fields.ToManyField('webservice.resources.news.NewsResource', 'latest_news', full=True)

    class Meta:
        queryset = Channel.objects.all()
        resource_name = 'subscription'
        serializer = Serializer(formats=['json'])
        paginator_class = AutoPaginator
        filtering = {
            'name' : ALL,
        }

    def get_object_list(self, request):
        return super(SubscriptionResource, self).get_object_list(request).all().order_by('subscriber')