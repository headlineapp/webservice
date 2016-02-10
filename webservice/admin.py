from django.contrib import admin
from .models import Channel, News, Subscriber

@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    pass

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    pass

@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    pass