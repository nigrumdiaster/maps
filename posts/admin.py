from django.contrib import admin
from .models import Post
from ckeditor.widgets import CKEditorWidget

class PostAdmin(admin.ModelAdmin):
    formfield_overrides = {
        Post.content.field.name: {'widget': CKEditorWidget},
    }

admin.site.register(Post, PostAdmin)