from webservice.models import *
from tastypie.serializers import Serializer
from tastypie.paginator import Paginator as AutoPaginator
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS


class SubscriberResource(ModelResource):
    class Meta:
        queryset = Subscriber.objects.all()
        resource_name = 'subscriber'
        serializer = Serializer(formats=['json'])
        paginator_class = AutoPaginator
