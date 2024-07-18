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
import json
from django.core.serializers.json import DjangoJSONEncoder

template_error = "404error.html"


class Create_journey(View):
    template_name = "journey/create_journey.html"

    def get(self, request):
        locations = Location.objects.all()
        data = {
            "locations": locations,
        }
        # Display the form for creating a journey
        return render(request, self.template_name, data)

    @csrf_exempt
    def post(self, request):
        try:
            journey_name = request.POST.get("journeyName")
            journey_description = request.POST.get("journeyDescription")
            journey_tags = request.POST.get("journeyTags")
            journey_song = request.POST.get("journeySong")
            uploaded_image = request.FILES.get("journeyImage")
            selected_location_ids = request.POST.getlist("locations")
            selected_locations = Location.objects.filter(id__in=selected_location_ids)

            # Download the audio
            downloader = YouTubeDownloader(journey_song)
            audio_path = downloader.download_audio()
            print(f"Downloaded audio file path: {audio_path}")

            # Save the audio file using Django's File system
            with open(audio_path, "rb") as audio_file:
                django_audio_file = File(audio_file)

                # Create a new Journey object
                new_journey = Journey(
                    name=journey_name,
                    description=journey_description,
                    image=uploaded_image,
                )
                new_journey.sound.save(os.path.basename(audio_path), django_audio_file)

                # Add tags to the new journey if provided
                if journey_tags:
                    tags = parse_tags(journey_tags)
                    new_journey.tags.add(*tags)
                    # Add locations to the new journey if provided
                new_journey.locations.set(selected_locations)
                # Save the new journey
                new_journey.save()

                if os.path.exists(audio_path):
                    os.remove(audio_path)
                    print(f"Deleted audio file path: {audio_path}")
                locations = Location.objects.all()
                data = {"success": "Tạo điểm đến thành công!", "locations": locations}

                # Redirect to a success page or the journey detail page
                return render(request, self.template_name, data)

        except Exception as e:
            error = {"error": "Không tạo được điểm đến!"}
            print(f"Error: {e}")
            return render(request, self.template_name, error)


class List_journey(View):
    template_name = "journey/list_journey.html"

    def get(self, request):
        try:
            journeys = Journey.objects.all().order_by("-id")
            paginator = Paginator(journeys, 10)  # Show 10 journeys per page

            page_number = request.GET.get("page")
            page_obj = paginator.get_page(page_number)
            data = {"page_obj": page_obj}

            return render(request, self.template_name, data)

        except Exception as e:
            print(f"Error: {e}")
            return render(request, template_error)


class Detail_journey(View):
    template_name = "journey/detail_journey.html"

    def get(self, request, pk):
        # try:
        # Retrieve the journey object
        journey = get_object_or_404(Journey, pk=pk)
        locations = journey.locations.all()

        locations_list = []
        for location in locations:
            image = location.images.first()
            locations_list.append(
                {
                    "name": location.name,
                    "description": location.description,
                    "address": location.address,
                    "latitude": location.latitude,
                    "longitude": location.longitude,
                    "image": (
                        image.images.url if image else None
                    ),  # Assuming 'image' has a 'url' attribute
                }
            )

        data = {
            "locations_json": json.dumps(locations_list, cls=DjangoJSONEncoder),
            "locations": locations,
            "journey": journey,
        }
        # Render the template with journey
        return render(request, self.template_name, data)

    # except Exception as e:
    #     print(f"Error: {e}")
    #     return render(request, template_error)


def edit_journey(request, pk):
    journey = get_object_or_404(Journey, pk=pk)
    locations = Location.objects.all()

    if request.method == "POST":
        selected_location_ids = request.POST.getlist("locations")
        selected_locations = Location.objects.filter(id__in=selected_location_ids)
        journey.locations.set(selected_locations)
        journey.save()
        return redirect("detail_journey", pk=journey.pk)

    data = {
        "journey": journey,
        "locations": locations,
    }

    return render(request, "journey/edit_journey.html", data)
