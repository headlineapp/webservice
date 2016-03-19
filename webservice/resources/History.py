from webservice.models import *
from tastypie.serializers import Serializer
from tastypie.resources import ModelResource, ALL_WITH_RELATIONS
from webservice.resources.news import NewsResource
from tastypie import fields


class HistoryResource(ModelResource):
    news = fields.ForeignKey(NewsResource, 'news', full=True)

    class Meta:
        queryset = History.objects.all()
        resource_name = 'history'
        serializer = Serializer(formats=['json'])
        filtering = {
            'news' : ALL_WITH_RELATIONS
        }
