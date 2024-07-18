from django.contrib import admin
from .views import Journey


# Register your models here.
@admin.register(Journey)
class JourneyAdmin(admin.ModelAdmin):

    def display_tags(self, obj):
        return ", ".join(tag.name for tag in obj.tags.all())

    display_tags.short_description = "Tags"  # Set column header for displayed tags
