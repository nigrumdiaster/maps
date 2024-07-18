from django.contrib import admin
from django.utils.html import format_html
from .models import Location, LocationImage, Category, LocationImage3D


class LocationImageInline(admin.TabularInline):
    model = LocationImage
    extra = 1


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("name", "address", "created_at", "views")
    search_fields = ("name", "address", "description")
    list_filter = ("created_at", "tags")
    inlines = [LocationImageInline]

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.views = 0  # Initialize views to 0 for new objects
        super().save_model(request, obj, form, change)

    def display_tags(self, obj):
        return ", ".join(tag.name for tag in obj.tags.all())

    display_tags.short_description = "Tags"  # Set column header for displayed tags


@admin.register(LocationImage)
class LocationImageAdmin(admin.ModelAdmin):
    list_display = ("location", "images")
    search_fields = ("location__name",)



    def images(self, obj):
        return format_html('<img src="{}" width="50" height="50" />', obj.images.url)
    images.short_description = 'Image'

admin.site.register(Category)

@admin.register(LocationImage3D)
class LocationImage3DAdmin(admin.ModelAdmin):
    list_display = ('location', 'images3D')
    search_fields = ('location__name',)

    def images3D(self, obj):
        return format_html('<img src="{}" width="50" height="50" />', obj.images3D.url)
    images3D.short_description = '3D Image'

