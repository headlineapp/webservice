from django.conf.urls import url
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, InvalidPage
from webservice.models import *
from tastypie import fields
from tastypie.serializers import Serializer
from tastypie.paginator import Paginator as AutoPaginator
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie.utils import trailing_slash
from django.http import Http404
from webservice.resources.pagination import prepare_results


class ChannelResource(ModelResource):
    class Meta:
        queryset = Channel.objects.all()
        resource_name = 'channel'
        serializer = Serializer(formats=['json'])
        paginator_class = AutoPaginator
        filtering = {
            'name' : ALL,
        }

    def prepend_urls(self):
        url_pattern = r"^(?P<resource_name>%s)/trending%s$" % (self._meta.resource_name, trailing_slash())
        return [
            url(url_pattern, self.wrap_view('get_trending_channel'), name="api_get_trending_channel"),
        ]

    def get_trending_channel(self, request, **kwargs):
        self.method_check(request, allowed=['get'])

        channels = Channel.objects.all().order_by('subscriber')
        object_list = prepare_results(self, request, channels)

        return self.create_response(request, object_list)