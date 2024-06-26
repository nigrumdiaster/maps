from django.shortcuts import render
from django.views import View
from django.core.paginator import Paginator
from destination.models import Location




# Create your views here.
template_error = '404error.html'
class Show_maps(View):
    template_name = 'maps/show_maps.html'
    def get(self, request):
        try:
            locations = Location.objects.all().order_by('-created_at')
            paginator = Paginator(locations, 10)  # Show 10 locations per page

            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            data = {'page_obj': page_obj}

            return render(request, self.template_name, data)
    
        except Exception as e:
            print(f"Error: {e}")
            return render(request, template_error)

