import os

from django.core import validators
from django.core.exceptions import ValidationError
from django.db import models

from api.utils.img import Util


def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]
    ext = ext.replace('.', '')
    valid_extensions = validators.get_available_image_extensions()
    valid_extensions += ['heif', 'heic']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension.')

class HeifmgurModelField(models.FileField):
    """Custom Model FileField with HEIF support
    Essentially a copy of ImageField with width_field, height_field update 
    functionality
    """

    validators = [validate_file_extension]
    descriptor = models.fields.files.ImageFileDescriptor

    def __init__(self, verbose_name=None, name=None, width_field=None, height_field=None, **kwargs):
        self.width_field, self.height_field = width_field, height_field
        super().__init__(verbose_name, name, **kwargs)

    def check(self, **kwargs):
        return [
            *super().check(**kwargs),
            *self._check_image_library_installed(),
        ]

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        if self.width_field:
            kwargs['width_field'] = self.width_field
        if self.height_field:
            kwargs['height_field'] = self.height_field
        return name, path, args, kwargs

    def contribute_to_class(self, cls, name, **kwargs):
        super().contribute_to_class(cls, name, **kwargs)
        if not cls._meta.abstract:
            models.signals.post_init.connect(self.update_dimension_fields, sender=cls)

    def _check_image_library_installed(self):
        try:
            from wand.image import Image  # NOQA
        except ImportError:
            return [
                checks.Error(
                    'Cannot use HeifmgurModelField because Wand is not installed.',
                    hint=('Get Wand at https://pypi.org/project/Wand/ '
                          'or run command "python -m pip install Wand".'),
                    obj=self,
                    id='fields.E210',
                )
            ]
        else:
            return []

    def update_dimension_fields(self, instance, force=False, *args, **kwargs):
        """
        Update field's width and height fields, if defined.
        """
 
        has_dimension_fields = self.width_field or self.height_field
        if not has_dimension_fields or self.attname not in instance.__dict__:
            return

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
            dimensions = Util.get_dimensions_from_file(file)
            width = dimensions[0]
            height = dimensions[1]
        else:
            width = None
            height = None

        # Update the width and height fields.
        if self.width_field:
            setattr(instance, self.width_field, width)
        if self.height_field:
            setattr(instance, self.height_field, height)
