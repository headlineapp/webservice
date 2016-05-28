import json
from django.http import HttpResponse
from .models import User, Channel, Subscription


def recommended_channel(request):
    idfa = request.GET['idfa']
    user = User.objects.get(IDFA=idfa)
    image_urls = Subscription.objects.filter(user=user).values_list('channel__profile_image_url')
    return HttpResponse(json.dumps({}), content_type = "application/json")
