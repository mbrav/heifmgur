import mimetypes
from io import BytesIO
from urllib import parse, request

from django.core.files import File
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image

HEADERS = {'User-Agent': 'Mozilla/5.0'}


class ResizeImage():
    """Класс для изменения размера изображения"""

    def __init__(self, image: str, width: int, height: int):
        self.image = image
        self.size = (width, height)

    def run(self, format: str = 'JPEG', quality: int = 90) -> File:
        image = Image.open(self.image)
        image.convert('RGB')
        image_io = BytesIO()
        new_image = image.resize(size=self.size)
        new_image.save(image_io, format, quality=quality)
        file = File(image_io, name=self.image)
        return file


class Util:
    """Утилиты для проекта app"""

    @staticmethod
    def resize_image(image, width: int, height: int):
        """Изменение размера изображения"""
        img_res = ResizeImage(image, width, height)
        return img_res.run()

    @staticmethod
    def parse_url_file_name(url: str, ext=False) -> str:
        """Парсер url минус extension (.html, .jpg, тд.)"""
        url = parse.urlparse(url)
        file_name = url.path.rsplit('/', 1)[-1]
        no_extension = file_name.rsplit('.', 1)[0]
        if ext and file_name != no_extension:
            return file_name
        return no_extension

    @staticmethod
    def download_img(url: str, django: bool = False):
        """Скачиваем изображение. Конвертирует в JPEG."""
        req = request.Request(url, headers=HEADERS)
        image = Image.open(request.urlopen(req))
        image = image.convert('RGB')
        image_name = Util.parse_url_file_name(url)
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
        return File(image_io)

    @ staticmethod
    def is_image_and_ready(url):
        """Проверяем URL изображения"""

        def is_url_image():
            """Проверяем что URL явлется изображением"""
            mimetype, encoding = mimetypes.guess_type(url)
            test = mimetypes.guess_extension(url)
            return (mimetype and mimetype.startswith('image'))

        def check_url():
            """Проверям работу URL"""
            try:
                req = request.Request(url, headers=HEADERS)
                response = request.urlopen(req)
                return response.status in range(200, 209)
            except Exception:
                return False

        return is_url_image() and check_url()


if __name__ == '__main__':
    # url = 'https://avatars.githubusercontent.com/u/1024025'
    url = 'https://www.w3.org/People/mimasa/test/imgformat/img/w3c_home.jpg'
    response = Util.is_image_and_ready(url)
    print(response)
    test = Util.download_img(url)
    print(test.tell())
