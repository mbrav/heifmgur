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
                {'error': 'Please provide a URL image file'})

        if attrs.get('url', None):
            good_url = Util.is_image_and_ready(attrs['url'])
            if not good_url:
                raise serializers.ValidationError(
                    {'error': 'URL validation error'})

        if attrs.get('picture', None):
            Util.is_image_validator(attrs['picture'])

        return attrs

    class Meta:
        model = Image
        fields = ('id', 'name', 'description', 'url', 'picture',
                  'width', 'height', 'parent_picture', 'date_created', 'date_updated')
        read_only_fields = ('height', 'width')


class ImageUpdateSerializer(serializers.ModelSerializer):
    """
    Image serializer for UPDATE queries

    Only name, description and parent_picture can be changed
    """

    def validate_parent_picture(self, parent_picture):
        if parent_picture.id == self.instance.id:
            raise serializers.ValidationError(
                {'error': 'Cannot assign a parent\'s picture to itself'})
        return parent_picture

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
        if value > 4000:
            raise serializers.ValidationError(
                'Cannot resize to over 4000 pixels.'
                'We are not a f***ing Google Data Center')

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
                            'picture', 'parent_picture', 'description')
