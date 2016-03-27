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
        resource_name = 'channel/all'
        serializer = Serializer(formats=['json'])
        paginator_class = AutoPaginator
        filtering = {
            'id': ALL,
            'name': ALL,
            'category': ALL_WITH_RELATIONS,
        }


class SubscriptionResource(ModelResource):
    class Meta:
        queryset = Channel.objects.all()
        resource_name = 'subscriptions'
        serializer = Serializer(formats=['json'])
        paginator_class = AutoPaginator

    def get_object_list(self, request):
        IDFA = request.GET.get('IDFA')
        subscribed_ids = Subscriber.objects.filter(IDFA=IDFA).values_list('channel__pk')
        return super(SubscriptionResource, self).\
            get_object_list(request).\
            filter(pk__in=subscribed_ids)