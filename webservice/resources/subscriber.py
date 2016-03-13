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
            'IDFA': ALL,
        }


    def obj_create(self, bundle, request=None, **kwargs):
        IDFA = bundle.data['IDFA']
        if IDFA:
            bundle.obj = Subscriber.objects.get_or_create(IDFA=IDFA)[0]
        else:
            raise BadRequest('Bad request')
        return bundle
