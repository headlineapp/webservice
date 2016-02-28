from django.conf.urls import url
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, InvalidPage
from webservice.models import *
from tastypie import fields
from tastypie.serializers import Serializer
from tastypie.paginator import Paginator as AutoPaginator
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie.utils import trailing_slash


class SubscriberResource(ModelResource):
    class Meta:
        queryset = Subscriber.objects.all()
        resource_name = 'subscriber'
        serializer = Serializer(formats=['json'])
        paginator_class = AutoPaginator
