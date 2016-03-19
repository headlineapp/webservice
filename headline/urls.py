from django.conf.urls import include, url
from django.contrib import admin
from tastypie.api import Api

from webservice.resources.channel import *
from webservice.resources.news import *
from webservice.resources.subscriber import *
from webservice.resources.bookmark import BookmarkResource
from webservice.resources.history import HistoryResource

from webservice.views import subscriber_detail, \
    subscribe_channel, \
    cancel_subscription, \
    update_history, \
    add_bookmark, \
    remove_bookmark

admin.site.site_title = 'Headline API'
admin.site.site_header = 'Headline API'

v1_api = Api(api_name='v1')
v1_api.register(NewsResource())
v1_api.register(LatestNewsResource())
v1_api.register(TrendingNewsResource())
v1_api.register(ChannelResource())
v1_api.register(SubscriberResource())
v1_api.register(BookmarkResource())
v1_api.register(HistoryResource())

urlpatterns = [
    url(r'^admin/$', admin.site.urls),
    url(r'^v1/subscriber/detail/(?P<idfa>.*)/$', subscriber_detail),
    url(r'^v1/subscriber/action/subscribe-channel/$', subscribe_channel),
    url(r'^v1/subscriber/action/cancel-subscription/$', cancel_subscription),
    url(r'^v1/news/action/update-history/$', update_history),
    url(r'^v1/news/action/add-bookmark/$', add_bookmark),
    url(r'^v1/news/action/remove-bookmark/$', remove_bookmark),
    url(r'^', include(v1_api.urls)),
]
