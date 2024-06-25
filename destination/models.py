from django.db import models
from taggit.managers import TaggableManager

class Location(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    tags = TaggableManager()
    created_at = models.DateTimeField(auto_now_add=True)
    address = models.CharField(max_length=255)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class LocationImage(models.Model):
    location = models.ForeignKey(Location, related_name='images', on_delete=models.CASCADE)
    images = models.FileField(upload_to = 'images/')

    def __str__(self):
        return self.location.name
