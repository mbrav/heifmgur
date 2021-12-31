import unittest
from pathlib import Path

import img

BASE_DIR = Path(__file__).resolve().parent.parent.parent
MEDIA_DIR = f'{BASE_DIR}/media'


class BaseTest(unittest.TestCase):
    image_path = f'{MEDIA_DIR}/logo.png'
    url = 'https://www.w3.org/People/mimasa/test/imgformat/img/w3c_home.jpg'


class PILImageTest(BaseTest):

    # def test_resize(self):
    #     image = img.PILImage(self.image_path)
    #     convert = image.convert_to_wand(format='jpeg')
    #     convert.rotate(90)
    #     image.get()._size
    #     convert.save(filename=f'convert.png')
    #     image = PILImage(image)
    #     image.resize(width, height)
    #     return image.get(django_file=django)

    def test_convert_Wand(self):
        image = img.PILImage(self.image_path)
        image.convert_to_wand()
        assert image.get().wand


class WandImageTest(BaseTest):

    def test_convert_PIL(self):
        image = img.WandImage(self.image_path)
        image.convert_to_PIL()
        assert image.get()._size == (1460, 366)

    def test_convert_to_heic(self):
        image = img.WandImage(self.image_path)
        image.convert_to('heic')
        converted_image = image.get()
        assert image.get().format == 'HEIC'


class URLImageTest(BaseTest):

    def test_check_url(self):
        image = img.URLImage(self.url)
        status = image.check_url()
        assert status == True

    def test_download(self):
        image = img.URLImage(self.url)
        image.download_img()
        image_name = image.get()._size
        assert image_name == (72, 48)


class UtilTest(BaseTest):
    pass


if __name__ == '__main__':
    unittest.main()
