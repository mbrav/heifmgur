
from django.contrib import admin

from .models import Image


@admin.register(Image)
class Image(admin.ModelAdmin):
    list_per_page = 50
    list_display = (
        'id',
        'name',
        'pub_date',
        'width',
        'height',
    )
    empty_value_display = '-пусто-'
    exclude = ('width', 'height',)
