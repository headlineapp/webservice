from webservice.models import *
from tastypie import fields
from tastypie.serializers import Serializer
from tastypie.resources import ModelResource, ALL_WITH_RELATIONS
from webservice.resources.news import NewsResource
from webservice.resources.user import UserResource
from tastypie.authorization import Authorization


class BookmarkResource(ModelResource):
    user = fields.ForeignKey(UserResource, 'user', full=True)
    news = fields.ForeignKey(NewsResource, 'news', full=True)

    class Meta:
        queryset = Bookmark.objects.all()
        resource_name = 'bookmark'
        serializer = Serializer(formats=['json'])
        authorization = Authorization()
        filtering = {
            'user' : ALL_WITH_RELATIONS,
            'news' : ALL_WITH_RELATIONS
        }
