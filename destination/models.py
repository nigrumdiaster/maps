from django.db import models
from taggit.managers import TaggableManager
import os
import hashlib
import datetime
from unidecode import unidecode


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Location(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    tags = TaggableManager()
    created_at = models.DateTimeField(auto_now_add=True)
    address = models.CharField(max_length=255)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    views = models.IntegerField(default=0)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="locations",
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name

    def first_image(self):
        return self.images.first().images.url if self.images.exists() else None


def get_image_upload_path(instance, filename):
    # Encode the filename using a hash function
    filename_base, filename_ext = os.path.splitext(filename)
    encoded_filename = hashlib.md5(
        (filename_base + datetime.datetime.now().isoformat()).encode("utf-8")
    ).hexdigest()

    # Convert location name to a suitable folder name
    location_name = unidecode(instance.location.name).replace(" ", "_")

    return "images/location/{}/{}{}".format(
        location_name, encoded_filename, filename_ext
    )


class LocationImage(models.Model):
    location = models.ForeignKey(
        Location, related_name="images", on_delete=models.CASCADE
    )
    images = models.FileField(upload_to=get_image_upload_path)

    def __str__(self):
        return self.location.name
