from webservice.models import *
from tastypie.serializers import Serializer
from tastypie.resources import ModelResource, ALL_WITH_RELATIONS
from tastypie.authorization import Authorization


class SubscriptionResource(ModelResource):
    class Meta:
        queryset = Subscription.objects.all()
        resource_name = 'subscription'
        serializer = Serializer(formats=['json'])
        always_return_data = True
        authorization = Authorization()
        filtering = {
            'user': ALL_WITH_RELATIONS,
            'channel': ALL_WITH_RELATIONS,
        }