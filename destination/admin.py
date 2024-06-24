from django.contrib import admin
from .models import Location, LocationImage

class LocationImageInline(admin.TabularInline):
    model = LocationImage
    extra = 1

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'created_at', 'views')
    search_fields = ('name', 'address', 'description')
    list_filter = ('created_at', 'tags')
    inlines = [LocationImageInline]

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.views = 0  # Initialize views to 0 for new objects
        super().save_model(request, obj, form, change)

    def display_tags(self, obj):
        return ", ".join(tag.name for tag in obj.tags.all())

    display_tags.short_description = 'Tags'  # Set column header for displayed tags

@admin.register(LocationImage)
class LocationImageAdmin(admin.ModelAdmin):
    list_display = ('location', 'images')
    search_fields = ('location__name',)
