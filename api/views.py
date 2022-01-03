from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Image
from .serializers import (ImageResizeSerializer, ImageSerializer,
                          ImageUpdateSerializer)
from .utils.img import Util


class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()

    def perform_create(self, serializer):
        """Download image via URL
        and automatically assign a name if it is not given"""

        new_data = serializer.validated_data
        new_data._mutable = True
        name = new_data.get('name')
        url = new_data.get('url')
        image = new_data.get('picture')

        if image:
            img_ext = Util.parse_file_extension(image.name)
            if img_ext not in ['heic', 'heif']:
                image = Util.convert_to_heic(image, django=True)
                new_data['picture'] = image
            if not name:
                new_data['name'] = image.name

        if url:
            image = Util.download_img(url, django=True, to_heif=True)
            new_data['picture'] = image
            if not name:
                new_data['name'] = image.name

        new_data._mutable = False
        serializer.save(**new_data)

    def destroy(self, request, **kwargs):
        image = self.get_object()
        try:
            image.picture.delete(save=False)
        except:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.perform_destroy(image)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post'])
    def resize(self, request, pk=None):
        """@action for resizing image"""

        image = self.get_object()
        serializer = serializer = self.get_serializer(
            image, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        new_dimensions = (
            int(request.data['width']),
            int(request.data['height']))
        image_path = image.picture.path
        image_name = Util.parse_file_name(
            image.picture.name, ext=True)
        new_image = Util.resize_image(
            image_path, *new_dimensions, django=True)
        image.picture.delete(save=False)
        image.picture.save(image_name, new_image)

        self.perform_update(serializer)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED)

    def get_serializer_class(self):
        # Custom serializer for resize
        if self.action == 'resize':
            return ImageResizeSerializer
        # Custom serializer for update
        if self.action == 'update':
            return ImageUpdateSerializer
        return ImageSerializer
