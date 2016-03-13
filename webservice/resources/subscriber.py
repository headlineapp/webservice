from webservice.models import *
from tastypie.serializers import Serializer
from tastypie.resources import ModelResource
from tastypie.exceptions import BadRequest
from tastypie.resources import ModelResource, ALL


class SubscriberResource(ModelResource):
    class Meta:
        queryset = Subscriber.objects.all()
        resource_name = 'subscriber'
        serializer = Serializer(formats=['json'])
        always_return_data = True
        filtering = {
            'uuid': ALL,
        }


    def obj_create(self, bundle, request=None, **kwargs):
        uuid = bundle.data['uuid']
        if uuid:
            bundle.obj = Subscriber.objects.get_or_create(uuid=uuid)[0]
        else:
            raise BadRequest('Bad request')
        return bundle
