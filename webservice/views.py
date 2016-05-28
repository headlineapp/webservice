import json
from django.http import HttpResponse
from .models import User, Channel, Subscription


def recommended_channel(request):
    identifier = request.GET['IDFA']
    user = User.objects.get(IDFA=identifier)
    subscribed_channels = Subscription.objects.filter(user=user).values_list('channel__pk', flat=True)
    image_urls = Channel.objects.all().exclude(pk__in=subscribed_channels).values_list('profile_image_url', flat=True)
    return HttpResponse(json.dumps(list(image_urls)[:3]), content_type = "application/json")
