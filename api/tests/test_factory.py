import random
from io import BytesIO

from app.models import Image as ImageModel
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.test import Client, TestCase
from PIL import Image, ImageDraw, ImageFont
from rest_framework.test import APIRequestFactory


class TestModelFactory(TestCase):
    """Обобществлённый завод для создания моделей"""

    @classmethod
    def createFunTestImage(self, name, size=None, color=None):
        """Создаём весёлые разноцветные картинки для тестов"""

        contrast_color = (0, 0, 0)
        if color is None:
            color = (
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255))
            contrast_color = tuple((c + 125) % 255 for c in color)
        if size is None:
            size = (
                random.randint(150, 300),
                random.randint(150, 300))

        img_name = f'fun-test-image-{name}.jpg'
        fnt = ImageFont.load_default()

        im = Image.new(mode='RGB', size=size, color=color)
        d = ImageDraw.Draw(im)

        for i in range(100):
            rand_size = (random.randint(
                0, size[0]), random.randint(0, size[1]))
            rand_letter = img_name[i % len(img_name)]
            rand_color = (random.randint(0, 255), random.randint(
                0, 255), random.randint(0, 255))
            d.multiline_text(rand_size, rand_letter, font=fnt, fill=rand_color)

        d.multiline_text((10, size[1] - 20), img_name,
                         font=fnt, fill=contrast_color)

        im_io = BytesIO()
        im.save(im_io, 'JPEG')
        im_io.seek(0)

        image = InMemoryUploadedFile(
            im_io, None, img_name, 'image/jpeg', len(im_io.getvalue()), None)
        return image

    @classmethod
    def setUpClass(self):
        super().setUpClass()
        self.guest_client = Client()
        self.rest_factory = APIRequestFactory()
        self.number_of_images = random.randint(5, 10)
        images = []
        for img in range(0, self.number_of_images):
            new_img = ImageModel(
                name=f'Тестовoe изображение №{img}',
                picture=self.createFunTestImage(f'{img}'),
                id=img
            )
            images.append(new_img)

        ImageModel.objects.bulk_create(objs=images, batch_size=100)
        self.image = ImageModel.objects.all().last()
