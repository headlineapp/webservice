from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from tastypie.api import Api

from webservice.resources.channel import *
from webservice.resources.news import *
from webservice.resources.user import *
from webservice.resources.bookmark import BookmarkResource
from webservice.resources.history import HistoryResource
from webservice.resources.category import CategoryResource
from webservice.resources.user import UserResource
from webservice.resources.subscription import SubscriptionResource
from webservice.views import recommended_channel


admin.site.site_title = 'Headline API'
admin.site.site_header = 'Headline API'

v1_api = Api(api_name='v1')

v1_api.register(UserResource())
v1_api.register(SubscriptionResource())

v1_api.register(NewsResource())
v1_api.register(BookmarkResource())
v1_api.register(HistoryResource())

v1_api.register(ChannelResource())
v1_api.register(CategoryResource())

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include(v1_api.urls)),
    url(r'^recommended-channel/', recommended_channel),
]
