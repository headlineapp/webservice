"""headline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from tastypie.api import Api

from webservice.resources.channel import ChannelResource, SubscriptionResource
from webservice.resources.news import NewsResource, LatestNewsResource, TrendingNewsResource
from webservice.resources.subscriber import SubscriberResource

admin.site.site_title = 'Headline API'
admin.site.site_header = 'Headline API'

v1_api = Api(api_name='v1')
v1_api.register(NewsResource())
v1_api.register(LatestNewsResource())
v1_api.register(TrendingNewsResource())
v1_api.register(ChannelResource())
v1_api.register(SubscriptionResource())
v1_api.register(SubscriberResource())

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include(v1_api.urls)),
]
