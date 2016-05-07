from webservice.models import *
from webservice.resources.channel import ChannelResource
from tastypie.serializers import Serializer
from tastypie.resources import ModelResource, ALL
from tastypie import fields
from tastypie.authorization import Authorization
from tastypie.exceptions import ApiFieldError


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

        def hydrate(self, bundle):
            for field_name, field_obj in self.fields.items():
                if field_name == 'resource_uri':
                    continue
                if not field_obj.blank and not bundle.data.has_key(field_name):
                    raise ApiFieldError("The '%s' field has no data and doesn't allow a default or null value." % field_name)
            return bundle
