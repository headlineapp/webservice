from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, InvalidPage
from django.http import Http404


def prepare_results(resource, request, objects):
        paginator = Paginator(objects, 20)

        page = request.GET.get('page')
        try:
            results = paginator.page(page)
        except PageNotAnInteger:
            results = paginator.page(1)
        except InvalidPage:
            raise Http404("Sorry, no results on that page.")
        except EmptyPage:
            results = paginator.page(paginator.num_pages)

        objects = []

        for result in results.object_list:
            bundle = resource.build_bundle(obj=result, request=request)
            bundle = resource.full_dehydrate(bundle)
            objects.append(bundle)

        object_list = {
            'objects': objects,
        }

        return object_list