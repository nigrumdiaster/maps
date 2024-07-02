from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from .models import Journey
from taggit.utils import parse_tags
from django.core.paginator import Paginator

template_error = '404error.html'
class Create_journey(View):
    template_name = 'journey/create_journey.html'
    
    def get(self, request):
        # Display the form for creating a journey
        return render(request, self.template_name)

    @csrf_exempt
    def post(self, request):
        try:
            journey_name = request.POST.get('journeyName')
            journey_description = request.POST.get('journeyDescription')
            journey_tags = request.POST.get('journeyTags')
            journey_song = request.POST.get('journeySong')
            uploaded_image = request.FILES.get('journeyImage')
            

            # Create a new Journey object and save it
            new_journey = Journey(
                name=journey_name,
                description=journey_description,
                sound_url=journey_song,
                image=uploaded_image
            )
            new_journey.save()
            # Add tags to the new journey if provided
            if journey_tags:
                tags = parse_tags(journey_tags)
                new_journey.tags.add(*tags)
            
            success = {
                'success': 'Tạo điểm đến thành công!'
            }

            # Redirect to a success page or the journey detail page
            return render(request, self.template_name, success)
        
        except Exception as e:
            error = {
                'error': 'Không tạo được điểm đến!'
            }
            print(f"Error: {e}")
            return render(request, self.template_name, error)
class List_journey(View):
    template_name = 'journey/list_journey.html'
    def get(self, request):
        try:
            journeys = Journey.objects.all().order_by('-id')
            paginator = Paginator(journeys, 10)  # Show 10 journeys per page

            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            data = {'page_obj': page_obj}

            return render(request, self.template_name, data)
    
        except Exception as e:
            print(f"Error: {e}")
            return render(request, template_error)


class Detail_journey(View):
    template_name = 'destination/detail_journey.html'

    def get(self, request, pk):
        try:
            # Retrieve the journey object
            journey = get_object_or_404(Journey, pk=pk)

            # Render the template with journey 
            return render(request, self.template_name, {'journey': journey})
        
        except Exception as e:
            print(f"Error: {e}")
            return render(request, template_error)