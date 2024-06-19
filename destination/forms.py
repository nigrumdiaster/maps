from django import forms
from .models import Location, LocationImage

class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['name', 'description', 'tags', 'image', 'address']

class LocationImageForm(forms.ModelForm):
    class Meta:
        model = LocationImage
        fields = ['images']
