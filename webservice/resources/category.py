from webservice.models import *
from tastypie.serializers import Serializer
from tastypie.paginator import Paginator as AutoPaginator
from tastypie.resources import ModelResource, ALL


class CategoryResource(ModelResource):
    class Meta:
        queryset = Category.objects.all()
        resource_name = 'category'
        serializer = Serializer(formats=['json'])
        paginator_class = AutoPaginator
        filtering = {
            'id': ALL,
            'name': ALL,
        }
