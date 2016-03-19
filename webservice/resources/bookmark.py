from webservice.models import *
from tastypie.serializers import Serializer
from tastypie.resources import ModelResource, ALL_WITH_RELATIONS
from webservice.resources.news import NewsResource
from tastypie import fields


class BookmarkResource(ModelResource):
    news = fields.ForeignKey(NewsResource, 'news', full=True)

    class Meta:
        queryset = Bookmark.objects.all()
        resource_name = 'bookmark'
        serializer = Serializer(formats=['json'])
        filtering = {
            'news' : ALL_WITH_RELATIONS
        }
