from webservice.models import *
from .channel import ChannelResource

from tastypie import fields
from tastypie.serializers import Serializer
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS


class NewsResource(ModelResource):
    channel = fields.ForeignKey(ChannelResource, 'channel', full=True)

    class Meta:
        queryset = News.objects.all()
        resource_name = 'news'
        serializer = Serializer(formats=['json'])
        filtering = {
            'id': ALL,
            'url_title': ALL,
            'channel': ALL_WITH_RELATIONS,
        }

    def get_object_list(self, request):
        IDFA = request.GET.get('IDFA')
        if IDFA:
            channels = Subscription.objects.filter(user__IDFA=IDFA).values_list('channel__id')
            return super(NewsResource, self).\
                get_object_list(request).\
                filter(channel__pk__in=channels).\
                exclude(url_title__isnull=True)
        else:
            return super(NewsResource, self).\
                get_object_list(request).\
                exclude(url_title__isnull=True)



