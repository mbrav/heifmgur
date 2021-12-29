from rest_framework import serializers

from .models import Image
from .utils import Util


class ImageSerializer(serializers.ModelSerializer):
    """
    Базовый Image сериализатор
    """

    def validate(self, attrs):
        if attrs.get('url', None) and attrs.get('picture', None):
            raise serializers.ValidationError(
                {'error': 'Вы мне можете оправить ссылку и фаил одновременно'})

        if not attrs.get('url', None) and not attrs.get('picture', None):
            raise serializers.ValidationError(
                {'error': 'Пожалуйста укажите ссылку либо фаил изображения'})

        if attrs.get('url', None):
            good_url = Util.is_image_and_ready(attrs['url'])
            if not good_url:
                raise serializers.ValidationError(
                    {'error': 'Ошибка валидации ссылки на изображение'})
        return attrs

    class Meta:
        model = Image
        fields = ('id', 'name', 'url', 'picture',
                  'width', 'height', 'parent_picture')
        read_only_fields = ('height', 'width')


class ImageUpdateSerializer(serializers.ModelSerializer):
    """
    Image сериализатор для UPDATE запросов
    + дополнительная функция

    Изменять можно только name и parent_picture
    """

    class Meta(ImageSerializer.Meta):
        read_only_fields = ('url', 'picture', 'height', 'width')


class ImageResizeSerializer(serializers.ModelSerializer):
    """
    Image сериализатор для resize запросов
    """

    def pixel_dimension(value):
        if value < 1:
            raise serializers.ValidationError(
                'Цифра должна быть не меньше 1')

    height = serializers.IntegerField(
        required=True,
        validators=[pixel_dimension],
    )

    width = serializers.IntegerField(
        required=True,
        validators=[pixel_dimension],
    )

    class Meta(ImageSerializer.Meta):
        read_only_fields = ('id', 'name', 'url',
                            'picture', 'parent_picture')
