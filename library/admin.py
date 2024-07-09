from django.contrib import admin
from .models import Image, Video

class ImageAdmin(admin.ModelAdmin):
    def Image(self, obj):
        return ", ".join(tag.name for tag in obj.tags.all())
admin.site.register(Image, ImageAdmin)

class VideoAdmin(admin.ModelAdmin):
    def Video(self, obj):
        return ", ".join(tag.name for tag in obj.tags.all())
admin.site.register(Video, VideoAdmin)
