from rest_framework import serializers

from .models import Image
from .utils.img import Util


class ImageSerializer(serializers.ModelSerializer):
    """
    Base Image serializer
    """

    picture = serializers.FileField(
        required=False,
    )

    def validate(self, attrs):
        if attrs.get('url', None) and attrs.get('picture', None):
            raise serializers.ValidationError(
                {'error': 'You cannot send a URL and a file at the same time'})

        if not attrs.get('url', None) and not attrs.get('picture', None):
            raise serializers.ValidationError(
                {'error': 'Please provide a URLr image file'})

        if attrs.get('url', None):
            good_url = Util.is_image_and_ready(attrs['url'])
            if not good_url:
                raise serializers.ValidationError(
                    {'error': 'URL validation error'})
        return attrs

    class Meta:
        model = Image
        fields = ('id', 'name', 'url', 'picture',
                  'width', 'height', 'parent_picture')
        read_only_fields = ('height', 'width')


class ImageUpdateSerializer(serializers.ModelSerializer):
    """
    Image serializer for UPDATE queries
    + additional function

    Only name and parent_picture can be changed
    """

    class Meta(ImageSerializer.Meta):
        read_only_fields = ('url', 'picture', 'height', 'width')


class ImageResizeSerializer(serializers.ModelSerializer):
    """
    Image serializer for resize requests
    """

    def pixel_dimension(value):
        if value < 1:
            raise serializers.ValidationError(
                'Number must not be lower than 1')

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
