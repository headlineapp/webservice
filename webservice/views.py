from django.http import HttpResponse
from webservice.resources.subscriber import SubscriberResource
from webservice.models import Channel
from django.views.decorators.csrf import csrf_exempt


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

    idfa = request.POST.get('IDFA')
    channel_id = request.POST.get('channel_id')
    user = res.obj_get(request_bundle, IDFA=idfa)
    channel = Channel.objects.get(pk=channel_id)
    user.channel.remove(channel)

    user_bundle = res.build_bundle(request=request, obj=user)
    user_json = res.serialize(None, res.full_dehydrate(user_bundle), "application/json")

    return HttpResponse(user_json, content_type='application/json')