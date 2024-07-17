from django.shortcuts import render
from django.views import View
from django.core.paginator import Paginator
from destination.models import Category, Location
import json
from django.core.serializers.json import DjangoJSONEncoder


template_error = '404error.html'

class Show_maps(View):
    template_name = 'maps/show_maps.html'
    
    def get(self, request):
        try:
            locations = Location.objects.all().order_by('-created_at')
            paginator = Paginator(locations, 10)  # Show 10 locations per page

            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)

            locations_list = []
            for location in page_obj:
                image = location.images.first()
                locations_list.append({
                    'name': location.name,
                    'address': location.address,
                    'latitude': location.latitude,
                    'longitude': location.longitude,
                    'image': image.images.url if image else None  # Assuming 'image' has a 'url' attribute
                })

            data = {
                'page_obj': page_obj,
                'locations_json': json.dumps(locations_list, cls=DjangoJSONEncoder),
            }

            return render(request, self.template_name, data)

        except Exception as e:
            print(f"Error: {e}")
            return render(request, template_error)
        
def Show_categories(request):
    template_name = 'maps/show_categories.html'
    categories = Category.objects.prefetch_related('locations').all()
    data = {
        "categories": categories
    }
    if request.method == "GET":
        locations = Location.objects.all()
        locations_list = []
        for location in locations:
            image = location.images.first()
            locations_list.append({
                'name': location.name,
                'address': location.address,
                'latitude': location.latitude,
                'longitude': location.longitude,
                'image': image.images.url if image else None  # Assuming 'image' has a 'url' attribute
            })
        data = {
            "categories": categories,
            'locations_json': json.dumps(locations_list, cls=DjangoJSONEncoder),
        }
        return render(request, template_name, data)
    elif request.method == "POST":
        return render(request, template_name, data)

def Navigation(request):
    template_name = 'maps/navigation.html'
    categories = Category.objects.prefetch_related('locations').all()
    data = {
        "categories": categories
    }
    if request.method == "GET":
        locations = Location.objects.all()
        locations_list = []
        for location in locations:
            image = location.images.first()
            locations_list.append({
                'name': location.name,
                'address': location.address,
                'latitude': location.latitude,
                'longitude': location.longitude,
                'image': image.images.url if image else None  # Assuming 'image' has a 'url' attribute
            })
        data = {
            "categories": categories,
            'locations_json': json.dumps(locations_list, cls=DjangoJSONEncoder),
        }
        return render(request, template_name, data)