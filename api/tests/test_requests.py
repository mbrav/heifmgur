from api.models import Image
from rest_framework.reverse import reverse
from rest_framework.test import APIRequestFactory

from .test_factory import TestModelFactory


class ImageURLTests(TestModelFactory):
    """Тест URL"""

    def test_images_list(self):
        """Страница /api/images/ доступна"""
        url = reverse('images-list')
        response = self.guest_client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_images_list_post(self):
        """Страница /api/images/ принимает POST запросы"""

        url = reverse('images-list')
        data = {
            'url': 'https://www.w3.org/People/mimasa/test/imgformat/img/w3c_home.jpg'
        }

        response = self.guest_client.post(url, data, format='json')
        count = Image.objects.all().count()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(count-1, self.number_of_images)
        self.number_of_images += 1

    def test_images_detail_get(self):
        """Страница /api/images/<id>/ доступна"""
        url = reverse('images-detail', args=[self.image.id])
        response = self.guest_client.get(url)
        self.assertEqual(response.status_code, 200)

    # def test_images_detail_put(self):
    #     """Страница /api/images/<id>/ принимает PUT запросы"""
    #     url = reverse('images-detail', args=[self.image.id])

    #     data = {
    #         'name': 'test_new_name'
    #     }

    #     request = self.rest_factory.put(url, data, format='json')
    #     response = self.guest_client.get(request)

    #     # self.assertEqual(response2.data, data)
    #     self.assertEqual(request.status_code, 201)

    def test_images_resize_get(self):
        """Страница /api/images/<id>/resize/ не принимает GET запросы"""
        url = reverse('images-detail', args=[self.image.id])
        response = self.guest_client.get(url+'resize/')
        self.assertEqual(response.status_code, 405)

    def test_images_resize_post(self):
        """Страница /api/images/<id>/resize/ принимает POST запросы
            и изменяет изображения
        """
        url = reverse('images-detail', args=[self.image.id])

        size = (self.image.width, self.image.height)
        name = self.image.picture.name
        response = self.guest_client.post(
            url+'resize/', {'width': 300, 'height': 200})

        self.image = Image.objects.get(id=self.image.id)
        new_size = (self.image.width, self.image.height)

        self.assertNotEqual(size, new_size)
        self.assertEqual(name, self.image.picture.name)
        self.assertEqual(300, new_size[0])
        self.assertEqual(200, new_size[1])
        self.assertEqual(response.status_code, 201)

    def test_images_id_delete_url(self):
        """Страница /api/images/<id>/ с DELETE запросом работает"""

        img_id = self.number_of_images // 2
        url = reverse('images-detail', args=[img_id])
        response = self.guest_client.delete(url)
        count = Image.objects.all().count()

        self.assertEqual(response.status_code, 204)
        self.assertEqual(count+1, self.number_of_images)
        self.number_of_images -= 1
