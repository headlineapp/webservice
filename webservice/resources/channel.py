from webservice.models import *
from tastypie import fields
from tastypie.serializers import Serializer
from tastypie.paginator import Paginator as AutoPaginator
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS


class ChannelResource(ModelResource):
    class Meta:
        queryset = Channel.objects.all()
        resource_name = 'channel/all'
        serializer = Serializer(formats=['json'])
        paginator_class = AutoPaginator
        filtering = {
            'name' : ALL,
        }

