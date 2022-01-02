import sys
import unittest
from pathlib import Path

from api.utils.img import PILImage, URLImage, WandImage

BASE_DIR = Path(__file__).resolve().parent.parent.parent
MEDIA_DIR = f'{BASE_DIR}/media'


class BaseTest(unittest.TestCase):
    image_path = f'{MEDIA_DIR}/logo.png'
    url = 'https://www.w3.org/People/mimasa/test/imgformat/img/w3c_home.jpg'


class PILImageTest(BaseTest):

    def test_resize(self):
        image = PILImage(self.image_path)
        size = (100, 200)
        assert image.get()._size != size, 'Image has the same size already'

        image.call_method(method='resize', size=size)
        assert image.get()._size == size, 'Image has not been resized to the specified dimensions'

    def test_convert_Wand(self):
        image = PILImage(self.image_path)
        image.convert_to_wand()
        assert image.get().wand, 'Image is not a Wand instance'


class WandImageTest(BaseTest):

    def test_resize(self):
        image = WandImage(self.image_path)
        size = (100, 200)
        assert image.get().size != size, 'Image has the same size already'

        # image.call_method(method='resize', width=size[0], height=size[1])
        # assert image.get()._size == size

    def test_convert_PIL(self):
        image = WandImage(self.image_path)
        image.convert_to_PIL()
        assert image.get()._size == (1460, 366), 'Wrong Image'

    def test_convert_to_heic(self):
        image = WandImage(self.image_path)
        image.convert_to('heic')
        converted_image = image.get()
        assert image.get().format == 'HEIC', 'Image was not converted to .heic format'


class URLImageTest(BaseTest):

    def test_check_url(self):
        image = URLImage(self.url)
        status = image.check_url()
        assert status == True, 'URL to Image is not available'

    def test_download(self):
        image = URLImage(self.url)
        image.download_img()
        image_name = image.get()._size
        assert image_name == (72, 48), 'URL to Image does not have the correct size'


class UtilTest(BaseTest):
    pass


if __name__ == '__main__':
    unittest.main()