from tastypie import fields

from webservice.models import *
from webservice.resources.user import UserResource
from webservice.resources.channel import ChannelResource
from tastypie.serializers import Serializer
from tastypie.resources import ModelResource, ALL_WITH_RELATIONS
from tastypie.authorization import Authorization


class SubscriptionResource(ModelResource):
    user = fields.ForeignKey(UserResource, 'user', full=True)
    channel = fields.ForeignKey(ChannelResource, 'channel', full=True)

    class Meta:
        queryset = Subscription.objects.all()
        resource_name = 'subscription'
        serializer = Serializer(formats=['json'])
        always_return_data = True
        allowed_methods = ['get', 'post']
        authorization = Authorization()
        filtering = {
            'user': ALL_WITH_RELATIONS,
            'channel': ALL_WITH_RELATIONS,
        }