from webservice.models import *
from tastypie import fields
from tastypie.serializers import Serializer
from tastypie.paginator import Paginator as AutoPaginator
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS


class ChannelResource(ModelResource):
    class Meta:
        queryset = Channel.objects.all()
        resource_name = 'channel/all'
        serializer = Serializer(formats=['json'])
        paginator_class = AutoPaginator
        filtering = {
            'name' : ALL,
        }


class SubscriptionResource(ModelResource):
    class Meta:
        queryset = Channel.objects.all()
        resource_name = 'subscriptions'
        serializer = Serializer(formats=['json'])
        paginator_class = AutoPaginator

    def get_object_list(self, request):
        IDFA = request.GET.get('IDFA')
        subscibed_ids = Subscriber.objects.filter(IDFA=IDFA).values_list('channel__pk')
        return super(SubscriptionResource, self).\
            get_object_list(request).\
            filter(pk__in=subscibed_ids)