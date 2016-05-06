from webservice.models import *
from tastypie.serializers import Serializer
from tastypie.resources import ModelResource, ALL_WITH_RELATIONS
from webservice.resources.news import NewsResource
from webservice.resources.subscriber import SubscriberResource
from tastypie import fields
from tastypie.authorization import Authorization


class HistoryResource(ModelResource):
    subscriber = fields.ForeignKey(SubscriberResource, 'subscriber', full=True)
    news = fields.ForeignKey(NewsResource, 'news', full=True)

    class Meta:
        queryset = History.objects.all()
        resource_name = 'history'
        serializer = Serializer(formats=['json'])
        authorization = Authorization()
        filtering = {
            'subscriber': ALL_WITH_RELATIONS,
            'news': ALL_WITH_RELATIONS
        }
