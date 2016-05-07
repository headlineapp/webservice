from webservice.models import *
from tastypie.serializers import Serializer
from tastypie.resources import ModelResource, ALL_WITH_RELATIONS
from webservice.resources.news import NewsResource
from webservice.resources.user import UserResource
from tastypie import fields
from tastypie.authorization import Authorization


class HistoryResource(ModelResource):
    user = fields.ForeignKey(UserResource, 'user', full=True)
    news = fields.ForeignKey(NewsResource, 'news', full=True)

    class Meta:
        queryset = History.objects.all()
        resource_name = 'history'
        serializer = Serializer(formats=['json'])
        authorization = Authorization()
        filtering = {
            'user': ALL_WITH_RELATIONS,
            'news': ALL_WITH_RELATIONS
        }

    def get_object_list(self, request):
        return super(NewsResource, self).\
            get_object_list(request).\
            distinct('news__id').\
            exclude(url_title__isnull=True)
