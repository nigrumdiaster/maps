from django import forms
from django.conf import settings

class CKEditorWidget(forms.Textarea):
    class Media:
        css = {
            'all': (
                settings.STATIC_URL + 'ckeditor/ckeditor5-build-classic/build/ckeditor.css',
            )
        }
        js = (
            settings.STATIC_URL + 'ckeditor/ckeditor5-build-classic/build/ckeditor.js',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.attrs['class'] = 'ckeditor'
