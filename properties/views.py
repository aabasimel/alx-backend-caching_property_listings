from django.views.decorators.cache import cache_page
from django.http import JsonResponse
from .utils import get_all_properties
from .models import Property


@cache_page(60*15)
def property_list(request):
    property=Property.objects.all().value(
       'id', 'title', 'description', 'price', 'location', 'created_at' 
    )
    return JsonResponse(list(property),safe=False)