from webservice.models import *
from webservice.resources.channel import ChannelResource
from tastypie.serializers import Serializer
from tastypie.exceptions import BadRequest
from tastypie.resources import ModelResource, ALL
from tastypie import fields
from tastypie.authorization import Authorization


class SubscriberResource(ModelResource):
    channel = fields.ToManyField(ChannelResource, 'channel', full=True)

    class Meta:
        queryset = Subscriber.objects.all()
        resource_name = 'subscriber'
        serializer = Serializer(formats=['json'])
        always_return_data = True
        authorization = Authorization()
        filtering = {
            'IDFA': ALL,
        }