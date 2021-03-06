from django.db import models

from .fields import HeifmgurModelField


class Image(models.Model):

    name = models.CharField(
        'Picture name',
        help_text='Specify name of the picture',
        max_length=255,
        blank=True,
    )

    description = models.TextField(
        'Description',
        help_text='Specify description for the picture',
        max_length=255,
        blank=True,
    )

    picture = HeifmgurModelField(
        'Image',
        help_text='Specify image file',
        upload_to='%Y/%m/%d',
        height_field='height',
        width_field='width',
        null=True,
        blank=True,
    )

    parent_picture = models.ForeignKey(
        'self',
        help_text='Specify parent picture',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    url = models.CharField(
        'External picture',
        help_text='Specify picture url',
        max_length=255,
        blank=True,
        null=True,
    )

    width = models.PositiveIntegerField(
        'Picture width',
        null=True,
    )

    height = models.PositiveIntegerField(
        'Picture height',
        null=True,
    )

    date_created = models.DateTimeField(
        'Upload Date',
        auto_now_add=True,
    )

    date_updated = models.DateTimeField(
        'Update Date',
        auto_now=True,
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Image'
        verbose_name_plural = 'Images'

    def __str__(self):
        return f'Image #{self.id}'
