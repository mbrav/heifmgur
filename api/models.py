from django.db import models


class Image(models.Model):

    picture = models.ImageField(
        'Картинка',
        help_text='Укажите фаил картинки',
        upload_to='%Y/%m/%d',
        height_field='height',
        width_field='width',
        null=True,
        blank=True,
    )

    parent_picture = models.ForeignKey(
        'self',
        help_text='Укажите родителя картинки',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    url = models.CharField(
        'Внешняя картинка',
        help_text='Укажите ссылку на внешнюю картинку',
        max_length=255,
        blank=True,
        null=True,
    )

    name = models.CharField(
        'Имя картинки',
        help_text='Укажите имя картинки',
        max_length=255,
        blank=True,
    )

    width = models.PositiveIntegerField(
        'Ширина Картинки',
        help_text='Ширина Картинки',
        null=True,
    )

    height = models.PositiveIntegerField(
        'Высота Картинки',
        help_text='Высота Картинки',
        null=True,
    )

    pub_date = models.DateTimeField(
        'Дата публикации картинки',
        help_text='Укажите дату публикации картинки',
        auto_now_add=True,
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Картинка'
        verbose_name_plural = 'Картинки'

    def __str__(self):
        return 'Картинка #%s' % (self.id, )
