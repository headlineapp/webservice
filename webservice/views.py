import datetime
from webservice.models import User, News, History, Bookmark
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse


@csrf_exempt
def update_history(request):
    IDFA = request.POST.get('IDFA')
    return JsonResponse({'IDFA': request})
    # news_id = request.POST.get('news_id')
    # user = User.objects.get(IDFA=IDFA)
    # news = News.objects.get(pk=news_id)
    # channel = news.channel
    # history, created = History.objects.get_or_create(user=user, news=news)
    # if history:
    #     number_of_visit = history.number_of_visit + 1
    #     now = datetime.datetime.now()
    #     History.objects.filter(user=user, news=news).\
    #         update(number_of_visit=number_of_visit, modified_date=now)
    # return JsonResponse({
    #     'id':history.pk,
    #     'news':{
    #         'id':news.pk,
    #         'resource_uri':"/v1/news/latest/%s/" % news.pk,
    #         'twitter_date_posted':news.twitter_date_posted,
    #         'twitter_favorite_count':news.twitter_favorite_count,
    #         'twitter_id':news.twitter_id,
    #         'twitter_retweet_count':news.twitter_retweet_count,
    #         'twitter_text':news.twitter_text,
    #         'url':news.url,
    #         'url_description':news.url_description,
    #         'url_image':news.url_image,
    #         'url_title':news.url_title,
    #         'channel':{
    #             'description':channel.description,
    #             'id':channel.pk,
    #             'name':channel.name,
    #             'photo_url':channel.profile_image_url,
    #             'resource_uri':'/v1/channel/all/%s/' % channel.pk,
    #             'twitter_last_date':channel.twitter_last_date,
    #             'twitter_screen_name':channel.twitter_screen_name,
    #             'twitter_since_id':channel.twitter_since_id,
    #             'url':channel.url,
    #         },
    #     },
    #     'number_of_visit':history.number_of_visit,
    #     'last_visit_date':history.modified_date
    # })


@csrf_exempt
def add_bookmark(request):
    IDFA = request.POST.get('IDFA')
    news_id = request.POST.get('news_id')
    user = User.objects.get(IDFA=IDFA)
    news = News.objects.get(pk=news_id)
    bookmark, created = Bookmark.objects.get_or_create(user=user, news=news)
    channel = news.channel
    return JsonResponse({
        'id':bookmark.pk,
        'user':'/v1/user/%s/' % user.pk,
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
                'photo_url':channel.profile_image_url,
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
    user = User.objects.get(IDFA=IDFA)
    news = News.objects.get(pk=news_id)
    queryset = Bookmark.objects.filter(user=user, news=news)
    queryset.delete()
    if queryset.count() == 0:
        return JsonResponse({'is_success':1})
    else:
        return JsonResponse({'is_success':0})

