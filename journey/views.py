from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from .models import Journey
from taggit.utils import parse_tags
from django.core.paginator import Paginator
from destination.models import Location
from .utils import YouTubeDownloader
import os
from django.core.files import File

template_error = '404error.html'
class Create_journey(View):
    template_name = 'journey/create_journey.html'
    
    def get(self, request):
        # Display the form for creating a journey
        return render(request, self.template_name)

    @csrf_exempt
    def post(self, request):
        journey_name = request.POST.get('journeyName')
        journey_description = request.POST.get('journeyDescription')
        journey_tags = request.POST.get('journeyTags')
        journey_song = request.POST.get('journeySong')
        uploaded_image = request.FILES.get('journeyImage')

        # Download the audio
        downloader = YouTubeDownloader(journey_song)
        audio_path = downloader.download_audio()
        print(f"Downloaded audio file path: {audio_path}")

            # Save the audio file using Django's File system
        with open(audio_path, 'rb') as audio_file:
            django_audio_file = File(audio_file)

            # Create a new Journey object
            new_journey = Journey(
                    name=journey_name,
                    description=journey_description,
                    image=uploaded_image
                )
            new_journey.sound.save(os.path.basename(audio_path), django_audio_file)

                # Add tags to the new journey if provided
            if journey_tags:
                tags = parse_tags(journey_tags)
                new_journey.tags.add(*tags)

            # Save the new journey
            new_journey.save()

            if os.path.exists(audio_path):
                os.remove(audio_path)
                print(f"Deleted audio file path: {audio_path}")

            success = {
                'success': 'Tạo điểm đến thành công!'
            }

            # Redirect to a success page or the journey detail page
            return render(request, self.template_name, success)
        
        # except Exception as e:
        #     error = {
        #         'error': 'Không tạo được điểm đến!'
        #     }
        #     print(f"Error: {e}")
        #     return render(request, self.template_name, error)
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
    template_name = 'journey/detail_journey.html'

    def get(self, request, pk):
        try:
            # Retrieve the journey object
            journey = get_object_or_404(Journey, pk=pk)

            # Render the template with journey 
            return render(request, self.template_name, {'journey': journey})
        
        except Exception as e:
            print(f"Error: {e}")
            return render(request, template_error)
        

def add_locations_to_journey(request, pk):
    journey = get_object_or_404(Journey, pk=pk)
    
    # Get locations that are not already associated with the journey
    locations = Location.objects.exclude(journeys=journey)

    if request.method == 'POST':
        selected_location_ids = request.POST.getlist('locations')
        selected_locations = Location.objects.filter(id__in=selected_location_ids)
        journey.locations.add(*selected_locations)
        journey.save()
        return redirect('detail_journey', pk=journey.pk)

    return render(request, 'journey/add_locations_to_journey.html', {'journey': journey, 'locations': locations})


