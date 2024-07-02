from django.shortcuts import get_object_or_404, render
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.utils import timezone
from taggit.utils import parse_tags


from .models import Location, LocationImage
from .utils import get_location_from_address


from pathlib import Path
import environ
import os


env = environ.Env()
environ.Env.read_env()


template_error = '404error.html'
class Create_location(View):
    template_name = 'destination/create_location.html'
    
    def get(self, request):
        # Display the form for creating a location
        return render(request, self.template_name)
    @csrf_exempt
    def post(self, request):
        try:
            location_name = request.POST.get('locationName')
            location_description = request.POST.get('locationDescription')
            location_tags = request.POST.get('locationTags')
            location_address = request.POST.get('locationAddress')
            uploaded_images = request.FILES.getlist('file')  
            
            bing_maps_key = env("BING_MAP_KEY")

            location_latitude, location_longitude = get_location_from_address(location_address, bing_maps_key)

          

            # Create a new Location object and save it
            new_location = Location(
                name=location_name,
                description=location_description,
                address=location_address,
                latitude=location_latitude,
                longitude=location_longitude
            )
            new_location.save()

            # Add tags to the new location if provided
            if location_tags:
                tags = parse_tags(location_tags)
                new_location.tags.add(*tags)

            # Process and save each uploaded image
            for image in uploaded_images:
                new_image = LocationImage(location=new_location, images=image)
                new_image.save()

            # Prepare context for rendering the template
            success = {
                'success': 'Tạo điểm đến thành công!'
            }
            return render(request, self.template_name, success)
        
        except Exception as e:
            error = {
                'error': 'Không tạo được điểm đến!'
            }
            print(f"Error: {e}")
            return render(request, self.template_name, error)
class List_location(View):
    template_name = 'destination/list_location.html'
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
        





class Detail_location(View):
    template_name = 'destination/detail_location.html'

    def get(self, request, pk):
        try:
            # Retrieve the location object
            location = get_object_or_404(Location, pk=pk)

            # Check if 'last_visit' exists in the session and calculate time difference
            last_visit_str = request.session.get('last_visit')
            if last_visit_str:
                last_visit = timezone.datetime.strptime(last_visit_str, '%Y-%m-%dT%H:%M:%S.%f%z')
                time_difference = timezone.now() - last_visit
                # If time difference is more than 5 minutes, increment view count
                if time_difference.total_seconds() > 300:  # 300 seconds = 5 minutes
                    location.views += 1
                    location.save()
                    # Update last_visit time in session
                    request.session['last_visit'] = timezone.now().isoformat()
            else:
                # Set last_visit time in session
                request.session['last_visit'] = timezone.now().isoformat()
                # Increment view count for the first visit
                location.views += 1
                location.save()

            # Retrieve all related images
            images = location.images.all()

            # Render the template with location and images
            return render(request, self.template_name, {'location': location, 'images': images})
        
        except Exception as e:
            print(f"Error: {e}")
            return render(request, template_error)
        




