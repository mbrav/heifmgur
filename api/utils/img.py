import mimetypes
from io import BytesIO
from operator import methodcaller
from urllib import parse, request

from django.core.files import File
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image
from wand.image import Image as Wand


def parse_file_name(path: str, ext: bool = False) -> str:
    """Parse path minus extension (.html, .jpg, etc.)"""
    url = parse.urlparse(path)
    file_name = url.path.rsplit('/', 1)[-1]
    no_extension = file_name.rsplit('.', 1)[0]
    if ext and file_name != no_extension:
        return file_name
    return no_extension


def parse_file_extension(path: str) -> str:
    """Get path extension .html, .jpg, etc."""
    url = parse.urlparse(path)
    extension = url.path.rsplit('.')[-1]
    return extension


class BaseImage():
    """Base Image class"""

    def __init__(self):
        self.image = None
        self.file = None

        self.format = 'jpeg'
        self.mode = 'RGB'
        self.quality = 90
        self.content_type = 'image/jpeg'

    def set_format_settings(
        self,
            format: str = None,
            mode: str = None,
            quality: int = None):

        if format:
            self.format = format
        if quality:
            self.quality = quality
        if mode:
            self.mode = mode


class PILImage(BaseImage):
    """Class for PIL Image"""

    def __init__(self, filename: str):
        super().__init__()
        self.image = Image.open(filename)
        self.format = self.image.format

    def call_method(self, *args, ** kwargs):
        method = kwargs.pop('method', None)
        if not method:
            raise AttributeError(
                'Must provide a method in str format as a kwarg for an PIL Image object')

        self.image.convert(mode=self.mode)
        caller = methodcaller(method, *args, **kwargs)
        self.image = caller(self.image)

    def convert_to_wand(self, format: str = None):
        """Convert a PIL image to a Wand image"""
        if not format:
            format = self.format
        image_io = BytesIO()
        self.image.save(image_io, format=format)
        blob = image_io.getvalue()
        self.image = Wand(blob=blob)

    def get(self, django_file: bool = False):
        if django_file:
            image_io = BytesIO()
            self.image.save(image_io, format=self.format, quality=self.quality)
            return File(image_io, name=self.image)
        return self.image


class WandImage(BaseImage):
    """Class for Imagemagick's Wand Image"""

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.image = Wand(*args, **kwargs)
        self.format = self.image.format
        if kwargs.get('filename', None):
            self.name = parse_file_name(kwargs.get('filename'))
        file = kwargs.get('file', None)
        if file:
            if file.url:
                name = parse_file_name(file.url)
                self.name = name

    def convert_to(self, format: str = None):
        if format == self.format:
            return
        if not format:
            format = self.format
        self.format = format
        self.image.format = format
        self.image.mode = self.mode
        self.image = self.image.convert(format=format)

    def call_method(self, *args, ** kwargs):
        method = kwargs.pop('method', None)
        if not method:
            raise AttributeError(
                'Must provide a method in str format as a kwarg for a Wand Image object')

        if method == 'resize':
            width = kwargs.pop('width', None)
            height = kwargs.pop('height', None)
            self.image.resize(width, height)
            return

        raise AttributeError(
            'New methods under work')

        # TODO
        # caller = methodcaller(method, *args, **kwargs)
        # caller(self.image)

    def convert_to_PIL(self):
        """Convert a Wand image to a PIL image"""
        pil_image = Image.open(BytesIO(self.image.make_blob()))
        self.image = pil_image

    def get(self, django_file: bool = False):
        if django_file:
            image_io = BytesIO(self.image.make_blob())
            django_image = InMemoryUploadedFile(
                file=image_io,
                name=f'{self.name}.{self.format}',
                field_name=None,
                content_type=self.content_type,
                size=image_io.getbuffer().nbytes,  # BytesIO
                charset=None,)
            return django_image
        return self.image

    def save(self):
        print(f'{self.name}.{self.format}')
        self.image.save(filename=f'{self.name}.{self.format}')


class URLImage(BaseImage):
    """Class for URL stuff"""

    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0'}

    def __init__(self, url: str):
        super().__init__()
        self.url = url
        self.request = request.Request(url, headers=self.HEADERS)
        self.name = parse_file_name(self.url)
        self.format = parse_file_extension(self.url)
        self.wand = None

    def download_img(self, to_heif: bool = False):
        """Download image"""
        req = request.urlopen(self.request)

        is_heif = self.format in ['heic', 'heif']
        if to_heif or is_heif:
            self.wand = WandImage(file=req)
            if not is_heif:
                self.wand.convert_to('heif')
                self.format = 'heif'
            self.wand.content_type = 'image/' + self.format
        else:
            image = Image.open(req)
            self.image = image.convert(self.mode)

    def check_url(self):
        """Check URL of the image"""

        is_url_image = check_url = False

        # Check that if the URL is an image
        mimetype, encoding = mimetypes.guess_type(self.url)
        is_url_image = (mimetype and mimetype.startswith('image'))

        # Check that the URL is working
        try:
            response = request.urlopen(self.request)
            check_url = response.status in range(200, 209)
        except Exception:
            check_url = False

        return is_url_image and check_url

    def get(self, django_file: bool = False):
        if django_file:
            image_io = None
            if self.wand:
                image_io = BytesIO(self.image.wand.make_blob())
            else:
                image_io = BytesIO()
                self.image.save(
                    image_io,
                    format=self.format,
                    quality=self.quality)

            django_image = InMemoryUploadedFile(
                file=image_io,
                name=f'{self.name}.{self.format}',
                field_name=None,
                content_type=self.content_type,
                size=image_io.getbuffer().nbytes,  # BytesIO
                charset=None,)

            return django_image
        return self.image


class Util:
    """Image and URL Utilities for api project"""

    @staticmethod
    def resize_image(path: str, width: int, height: int, django: bool = False):
        """Change image size with Wand library"""
        image = WandImage(filename=path)
        image.call_method(method='resize', width=width, height=height)
        return image.get(django_file=django)

    @staticmethod
    def resize_image_PIL(path: str, width: int, height: int, django: bool = False):
        """Change image size with PIL library"""
        image = PILImage(path)
        image.call_method(method='resize', size=(width, height))
        return image.get(django_file=django)

    @staticmethod
    def parse_file_name(path: str, ext: bool = False) -> str:
        return parse_file_name(path, ext)

    @staticmethod
    def get_dimensions_from_path(path: str) -> tuple:
        """Get dimensions of a image URL"""
        image = WandImage(filename=path)
        dimensions = (image.image.width, image.image.height)
        return dimensions

    @staticmethod
    def get_dimensions_from_file(file: File) -> tuple:
        """Get dimensions of a image file"""
        image = WandImage(blob=file.file)
        dimensions = (image.image.width, image.image.height)
        return dimensions

    @staticmethod
    def download_img(url: str, django: bool = False, to_heif: bool = False):
        url_img = URLImage(url)
        url_img.download_img(to_heif=to_heif)

        # If image to heif is enforced and image is not in heif format
        if to_heif:
            return url_img.wand.get(django_file=django)
        return url_img.get(django_file=django)

    @staticmethod
    def is_image_and_ready(url: str):
        image = URLImage(url)
        return image.check_url()
