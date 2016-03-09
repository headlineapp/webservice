from django.contrib import admin
from .models import Channel, News, Subscriber, Country, Category
from django.template.defaultfilters import truncatechars  # or truncatewords
from pytz import timezone
from django.contrib.humanize.templatetags.humanize import naturaltime


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

    def get_number_of_channel(self, obj):
        return Channel.objects.filter(category=obj).count()
    get_number_of_channel.short_description = 'Channels'


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_number_of_channel', 'get_number_of_subscriber')

    def get_number_of_channel(self, obj):
        return Channel.objects.filter(country=obj).count()
    get_number_of_channel.short_description = 'Channels'

    def get_number_of_subscriber(self, obj):
        return Subscriber.objects.filter(country=obj).count()
    get_number_of_subscriber.short_description = 'Subcribers'


def delete_all_news(modeladmin, request, queryset):
    queryset.update(twitter_since_id=None)
    News.objects.all().delete()
delete_all_news.short_description = "Delete news for selected channels"


def delete_untitled_news(modeladmin, request, queryset):
    News.objects.filter(url_title__isnull=True).delete()
delete_untitled_news.short_description = "Delete untitled news for selected channels"


@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    list_display = ('name',
                    'get_screen_name',
                    'get_number_of_news',
                    'get_number_of_news_without_title',
                    'get_number_of_news_without_image',
                    'get_number_of_subscriber',
                    'get_url',
                    'get_last_tweet',
                    'get_last_tweet_date')
    actions = [delete_all_news, delete_untitled_news]

    def get_screen_name(self, obj):
        return '@%s' % obj.twitter_screen_name
    get_screen_name.short_description = 'Screen Name'

    def get_url(self, obj):
        return '<a href="%s" target="_blank">%s</a>' % (obj.url, obj.url)
    get_url.short_description = 'URL'
    get_url.allow_tags = True

    def get_number_of_news(self, obj):
        return News.objects.filter(channel=obj).count()
    get_number_of_news.short_description = 'News'

    def get_number_of_news_without_title(self, obj):
        return News.objects.filter(channel=obj, url_title__isnull=True).count()
    get_number_of_news_without_title.short_description = 'News W/O Title'

    def get_number_of_news_without_image(self, obj):
        return News.objects.filter(channel=obj, url_image__isnull=True).count()
    get_number_of_news_without_image.short_description = 'News W/O Image'

    def get_number_of_subscriber(self, obj):
        return obj.subscriber.count()
    get_number_of_subscriber.short_description = 'Subscriber'

    def get_last_tweet(self, obj):
        values = (obj.twitter_screen_name, obj.twitter_since_id, obj.twitter_since_id)
        return '<a href="https://twitter.com/%s/status/%s" target="_blank">%s</a>' % values
    get_last_tweet.short_description = 'Last News'
    get_last_tweet.allow_tags = True

    def get_last_tweet_date(self, obj):
        if obj.twitter_last_date:
            return naturaltime(obj.twitter_last_date)
        return None
    get_last_tweet_date.short_description = 'Last News Date'


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('get_channel', 'url_title', 'url_description', 'url_image', 'get_url_display', 'twitter_date_posted')

    def get_channel(self, obj):
        if obj.channel:
            return obj.channel.name
        return ''
    get_channel.short_description = 'Channel'

    def get_title(self, obj):
        if obj.url_title:
            return truncatechars(obj.url_title, 50)
        return ''
    get_title.short_description = 'Title'

    def get_text(self, obj):
        if obj.url_description:
            return truncatechars(obj.url_description, 20)
        return ''
    get_text.short_description = 'Text'

    def get_date_created(self, obj):
        if obj.twitter_date_posted:
            jakarta_timezone = timezone('Asia/Jakarta')
            date_posted = jakarta_timezone.normalize(obj.twitter_date_posted)
            return date_posted.strftime("%d/%m/%Y %H:%M")
        return None
    get_date_created.short_description = 'Date'

    def get_url_display(self, obj):
        return '<a href="%s" target="_blank">URL</a>' % obj.url
    get_url_display.short_description = 'URL'
    get_url_display.allow_tags = True


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'get_subscriber_id', 'get_number_of_subscriptions')

    def get_subscriber_id(self, obj):
        return obj.pk
    get_subscriber_id.short_description = 'ID'

    def get_number_of_subscriptions(self, obj):
        channels = Channel.objects.filter(subscriber__uuid=obj.uuid).values_list('name', flat=True)
        channels_name = '<br> '.join([str(x) for x in channels])
        number_of_subscriptions = len(channels)
        return '%d Channels<br>%s' % (number_of_subscriptions, channels_name)
    get_number_of_subscriptions.short_description = 'Subscriptions'
    get_number_of_subscriptions.allow_tags = True


