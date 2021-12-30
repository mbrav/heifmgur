import os

from django.core import validators
from django.core.exceptions import ValidationError
from django.db import models


def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]
    ext = ext.replace('.', '')
    valid_extensions = validators.get_available_image_extensions()
    valid_extensions += ['heif', 'heic']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension.')


class HeifmgurField(models.ImageField):
    """Custom ImageField for HEIF suport"""

    validators = [validate_file_extension]

    def update_dimension_fields(self, instance, force=False, *args, **kwargs):
        """
        Update field's width and height fields, if defined.
        """

        file = getattr(instance, self.attname)

        if not file and not force:
            return

        dimension_fields_filled = not(
            (self.width_field and not getattr(instance, self.width_field)) or
            (self.height_field and not getattr(instance, self.height_field))
        )

        if dimension_fields_filled and not force:
            return

        if file:
            width = file.width
            height = file.height
        else:
            width = None
            height = None

        if self.width_field:
            setattr(instance, self.width_field, width)
        if self.height_field:
            setattr(instance, self.height_field, height)
