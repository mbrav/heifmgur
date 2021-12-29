import mimetypes
from io import BytesIO
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


class PILImage():
    """Class for PIL Image"""

    def __init__(self, image: str):
        self.image = Image.open(image)

    def resize(self, width: int, height: int, format: str = 'JPEG', quality: int = 90) -> File:
        self.image.convert('RGB')
        image_io = BytesIO()
        new_image = self.image.resize(size=(width, height))
        new_image.save(image_io, format, quality=quality)
        file = File(image_io, name=self.image)
        return file


class WandImage():
    """Class for Imagemagick's Wand Image"""

    def __init__(self, image: str):
        self.image = Wand(filename=image)

    def convert_to(self, format: str, name: str):
        name = parse_file_name(name)
        image_convert = self.image.convert(format)
        image_convert.save(filename=f'{name}.{format}')


class URLImage():
    """Class for URL stuff"""

    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0'}

    def __init__(self, url: str):
        self.url = url
        self.request = request.Request(url, headers=self.HEADERS)

    def download_img(self, django: bool = False):
        """Download image, converts to JPEG."""
        image = Image.open(request.urlopen(self.request))
        image = image.convert('RGB')
        image_name = parse_file_name(self.url)
        image_io = BytesIO()
        # image.seek(0)
        image.save(image_io, format='JPEG')
        # image.save("test.jpg")
        # image.seek(0)

        if django:
            django_image = InMemoryUploadedFile(
                file=image_io,
                name=image_name,
                field_name=None,
                content_type='image/jpeg',
                size=image_io.getbuffer().nbytes,  # BytesIO
                charset=None,
            )
            return django_image
        return image_io

    def is_image_and_ready(self):
        """Check URL of the image"""

        def is_url_image():
            """Check that if the URL is an image"""
            mimetype, encoding = mimetypes.guess_type(self.url)
            test = mimetypes.guess_extension(self.url)
            return (mimetype and mimetype.startswith('image'))

        def check_url():
            """Check that the URL is working"""
            try:
                response = request.urlopen(self.request)
                return response.status in range(200, 209)
            except Exception:
                return False

        return is_url_image() and check_url()


class Util:
    """Image and URL Utilities for api project"""

    @staticmethod
    def resize_image(image, width: int, height: int):
        """Change image size"""
        image = PILImage(image)
        return image.resize(width, height)

    @staticmethod
    def parse_file_name(path: str, ext: bool = False) -> str:
        return parse_file_name(path, ext)

    @staticmethod
    def download_img(url: str, django: bool = False):
        image = URLImage(url)
        return image.download_img(django)

    @staticmethod
    def is_image_and_ready(url: str):
        image = URLImage(url)
        return image.is_image_and_ready()


if __name__ == '__main__':
    # url = 'https://avatars.githubusercontent.com/u/1024025'
    url = 'https://www.w3.org/People/mimasa/test/imgformat/img/w3c_home.jpg'
    response = Util.is_image_and_ready(url)
    print(response)
    test = Util.download_img(url)
    print(test.tell())