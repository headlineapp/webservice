import datetime
from django.http import HttpResponse
from webservice.resources.subscriber import SubscriberResource
from webservice.models import Subscriber, Channel, News, History, Bookmark
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse


def subscriber_detail(request, idfa):
    res = SubscriberResource()
    request_bundle = res.build_bundle(request=request)
    user = res.obj_get(request_bundle, IDFA=idfa)

    user_bundle = res.build_bundle(request=request, obj=user)
    user_json = res.serialize(None, res.full_dehydrate(user_bundle), "application/json")

    return HttpResponse(user_json, content_type='application/json')


@csrf_exempt
def subscribe_channel(request):
    res = SubscriberResource()
    request_bundle = res.build_bundle(request=request)

    idfa = request.POST.get('IDFA')
    channel_id = request.POST.get('channel_id')
    user = res.obj_get(request_bundle, IDFA=idfa)
    channel = Channel.objects.get(pk=channel_id)
    user.channel.add(channel)

    user_bundle = res.build_bundle(request=request, obj=user)
    user_json = res.serialize(None, res.full_dehydrate(user_bundle), "application/json")

    return HttpResponse(user_json, content_type='application/json')


@csrf_exempt
def cancel_subscription(request):
    res = SubscriberResource()
    request_bundle = res.build_bundle(request=request)

    IDFA = request.POST.get('IDFA')
    channel_id = request.POST.get('channel_id')
    user = res.obj_get(request_bundle, IDFA=IDFA)
    channel = Channel.objects.get(pk=channel_id)
    user.channel.remove(channel)

    user_bundle = res.build_bundle(request=request, obj=user)
    user_json = res.serialize(None, res.full_dehydrate(user_bundle), "application/json")

    return HttpResponse(user_json, content_type='application/json')


@csrf_exempt
def update_history(request):
    IDFA = request.POST.get('IDFA')
    news_id = request.POST.get('news_id')
    subscriber = Subscriber.objects.get(IDFA=IDFA)
    news = News.objects.get(pk=news_id)
    channel = news.channel
    history, created = History.objects.get_or_create(subscriber=subscriber, news=news)
    if history:
        number_of_visit = history.number_of_visit + 1
        now = datetime.datetime.now()
        History.objects.filter(subscriber=subscriber, news=news).\
            update(number_of_visit=number_of_visit, modified_date=now)
    return JsonResponse({
        'subscriber':'/v1/subscriber/%s/' % subscriber.pk,
        'news':{
            'id':news.pk,
            'resource_uri':"/v1/news/latest/%s/" % news.pk,
            'twitter_date_posted':news.twitter_date_posted,
            'twitter_favorite_count':news.twitter_favorite_count,
            'twitter_id':news.twitter_id,
            'twitter_retweet_count':news.twitter_retweet_count,
            'twitter_text':news.twitter_text,
            'url':news.url,
            'url_description':news.url_description,
            'url_image':news.url_image,
            'url_title':news.url_title,
            'channel':{
                'description':channel.description,
                'id':channel.pk,
                'name':channel.name,
                'photo_url':channel.photo_url,
                'resource_uri':'/v1/channel/all/%s/' % channel.pk,
                'twitter_last_date':channel.twitter_last_date,
                'twitter_screen_name':channel.twitter_screen_name,
                'twitter_since_id':channel.twitter_since_id,
                'url':channel.url,
            },
        },
        'number_of_visit':history.number_of_visit,
        'last_visit_date':history.modified_date
    })


@csrf_exempt
def add_bookmark(request):
    IDFA = request.POST.get('IDFA')
    news_id = request.POST.get('news_id')
    subscriber = Subscriber.objects.get(IDFA=IDFA)
    news = News.objects.get(pk=news_id)
    bookmark, created = Bookmark.objects.get_or_create(subscriber=subscriber, news=news)
    channel = news.channel
    return JsonResponse({
        'id':bookmark.pk,
        'subscriber':'/v1/subscriber/%s/' % subscriber.pk,
        'news':{
            'id':news.pk,
            'resource_uri':"/v1/news/latest/%s/" % news.pk,
            'twitter_date_posted':news.twitter_date_posted,
            'twitter_favorite_count':news.twitter_favorite_count,
            'twitter_id':news.twitter_id,
            'twitter_retweet_count':news.twitter_retweet_count,
            'twitter_text':news.twitter_text,
            'url':news.url,
            'url_description':news.url_description,
            'url_image':news.url_image,
            'url_title':news.url_title,
            'channel':{
                'description':channel.description,
                'id':channel.pk,
                'name':channel.name,
                'photo_url':channel.photo_url,
                'resource_uri':'/v1/channel/all/%s/' % channel.pk,
                'twitter_last_date':channel.twitter_last_date,
                'twitter_screen_name':channel.twitter_screen_name,
                'twitter_since_id':channel.twitter_since_id,
                'url':channel.url,
            },
        },
        'created_date':bookmark.created_date,
    })


@csrf_exempt
def remove_bookmark(request):
    IDFA = request.POST.get('IDFA')
    news_id = request.POST.get('news_id')
    subscriber = Subscriber.objects.get(IDFA=IDFA)
    news = News.objects.get(pk=news_id)
    queryset = Bookmark.objects.filter(subscriber=subscriber, news=news)
    queryset.delete()
    if queryset.count() == 0:
        return JsonResponse({'success':1})
    else:
        return JsonResponse({'success':0})

