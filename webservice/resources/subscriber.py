from webservice.models import *
from webservice.resources.channel import ChannelResource
from tastypie.serializers import Serializer
from tastypie.exceptions import BadRequest
from tastypie.resources import ModelResource, ALL
from tastypie import fields


class SubscriberResource(ModelResource):
    channel = fields.ToManyField(ChannelResource, 'channel', full=True)

    class Meta:
        queryset = Subscriber.objects.all()
        resource_name = 'subscriber'
        serializer = Serializer(formats=['json'])
        always_return_data = True
        filtering = {
            'IDFA': ALL,
        }


    def obj_create(self, bundle, request=None, **kwargs):
        IDFA = bundle.data['IDFA']
        if IDFA:
            bundle.obj = Subscriber.objects.get_or_create(IDFA=IDFA)[0]
        else:
            raise BadRequest('Bad request')
        return bundle
