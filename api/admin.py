
from django.contrib import admin

from .models import Image


@admin.register(Image)
class Image(admin.ModelAdmin):
    list_per_page = 50
    list_display = (
        'id',
        'name',
        'description',
        'width',
        'height',
        'date_created',
        'date_updated',
    )
    empty_value_display = '-empty-'
    exclude = ('width', 'height',)
