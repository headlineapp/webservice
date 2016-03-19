from webservice.models import *
from webservice.resources.channel import ChannelResource
from tastypie.serializers import Serializer
from tastypie.exceptions import BadRequest
from tastypie.resources import ModelResource, ALL
from tastypie import fields
from tastypie.utils import trailing_slash

from django.conf.urls import url


class SubscriberResource(ModelResource):
    channel = fields.ToManyField(ChannelResource, 'channel', full=True)

    class Meta:
        queryset = Subscriber.objects.all()
        resource_name = 'subscriber'
        serializer = Serializer(formats=['json'], content_types={'json': 'application/json'})
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

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/detail%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('subscriber_detail'), name="api_subscriber_detail"),
        ]

    def subscriber_detail(self, request, **kwargs):
        bundle = self.build_bundle(obj=Subscriber.objects.get(pk=1), request=request)
        return self.create_response(request, bundle)

