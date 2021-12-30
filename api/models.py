from django.db import models

from .fields import HeifmgurField


class Image(models.Model):

    picture = HeifmgurField(
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

    name = models.CharField(
        'Picture name',
        help_text='Specify name of the picture',
        max_length=255,
        blank=True,
    )

    width = models.PositiveIntegerField(
        'Picture width',
        null=True,
    )

    height = models.PositiveIntegerField(
        'Picture height',
        null=True,
    )

    pub_date = models.DateTimeField(
        'Date of publication',
        auto_now_add=True,
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Image'
        verbose_name_plural = 'Images'

    def __str__(self):
        return f'Image #{self.id}'
