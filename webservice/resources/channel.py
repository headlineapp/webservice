from webservice.models import *
from tastypie import fields
from tastypie.serializers import Serializer
from tastypie.paginator import Paginator as AutoPaginator
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from webservice.resources.category import CategoryResource


class ChannelResource(ModelResource):
    category = fields.ToManyField(CategoryResource, 'category', full=True)

    class Meta:
        queryset = Channel.objects.all()
        resource_name = 'channel'
        serializer = Serializer(formats=['json'])
        paginator_class = AutoPaginator
        filtering = {
            'id': ALL,
            'name': ALL,
            'category': ALL_WITH_RELATIONS,
        }

    def get_object_list(self, request):
        IDFA = request.GET.get('IDFA')
        if IDFA:
            channels = Subscription.objects.filter(user__IDFA=IDFA).values_list('channel__id')
            return super(ChannelResource, self).\
                get_object_list(request).\
                exclude(channel__pk__in=channels)
        else:
            return super(ChannelResource, self).get_object_list(request)