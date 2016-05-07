from webservice.models import *
from tastypie.serializers import Serializer
from tastypie.resources import ModelResource, ALL
from tastypie.authorization import Authorization


class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        serializer = Serializer(formats=['json'])
        always_return_data = True
        allowed_methods = ['get', 'post']
        authorization = Authorization()
        filtering = {
            'IDFA': ALL,
        }