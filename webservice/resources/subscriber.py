from webservice.models import *
from webservice.resources.channel import ChannelResource
from tastypie.serializers import Serializer
from tastypie.exceptions import BadRequest
from tastypie.resources import ModelResource, ALL
from tastypie import fields


class SubscriberResource(ModelResource):
    channel = fields.ToManyField(ChannelResource, 'channel', full=True)

    class Meta:
        queryset = Subscriber.objects.all()
        resource_name = 'subscriber'
        serializer = Serializer(formats=['json'], content_types={'json': 'application/json'})
        always_return_data = True
        filtering = {
            'IDFA': ALL,
        }

    def obj_create(self, bundle, request=None, **kwargs):
        IDFA = bundle.data['IDFA']
        if IDFA:
            bundle.obj = Subscriber.objects.get_or_create(IDFA=IDFA)[0]
        else:
            raise BadRequest('Bad request')
        return bundle

    def save_m2m(self, bundle):
        for field_name, field_object in self.fields.items():
            if not getattr(field_object, 'is_m2m', False):
                continue

            if not field_object.attribute:
                continue

            if field_object.readonly:
                continue

            related_mngr = getattr(bundle.obj, field_object.attribute)

            related_objs = []

            for related_bundle in bundle.data[field_name]:
                channel, found = Channel.objects.get_or_create(pk=related_bundle.obj.pk)
                if found:
                    channel.delete()
                else:
                    channel = related_bundle.obj
                    channel.save()

                related_objs.append(channel)

            related_mngr.add(*related_objs)
