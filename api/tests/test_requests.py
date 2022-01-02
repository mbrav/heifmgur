from api.models import Image
from rest_framework.reverse import reverse
from rest_framework.test import APIRequestFactory

from .test_factory import TestModelFactory


class ImageURLTests(TestModelFactory):
    """Тест URL"""

    def test_images_list(self):
        """The page/api/images/is available"""
        url = reverse('images-list')
        response = self.guest_client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_images_list_post(self):
        """The page/api/images/accepts POST requests"""

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
        """The page/api/images/<id>/ is available"""
        url = reverse('images-detail', args=[self.image.id])
        response = self.guest_client.get(url)
        self.assertEqual(response.status_code, 200)

    # def test_images_detail_put(self):
    #     """The page/api/images/<id>/ accepts PUT requests"""
    #     url = reverse('images-detail', args=[self.image.id])

    #     data = {
    #         'name': 'test_new_name'
    #     }

    #     request = self.rest_factory.put(url, data, format='json')
    #     response = self.guest_client.get(request)

    #     # self.assertEqual(response2.data, data)
    #     self.assertEqual(request.status_code, 201)

    def test_images_resize_get(self):
        """The page/api/images/<id>/resize/ does not accept GET requests"""
        url = reverse('images-detail', args=[self.image.id])
        response = self.guest_client.get(url+'resize/')
        self.assertEqual(response.status_code, 405)

    def test_images_resize_post(self):
        """The page /api/images/<id>/resize/ accepts POST requests
        and changes images
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
        """The page /api/images/<id>/ works with a DELETE request"""

        img_id = self.number_of_images // 2
        url = reverse('images-detail', args=[img_id])
        response = self.guest_client.delete(url)
        count = Image.objects.all().count()

        self.assertEqual(response.status_code, 204)
        self.assertEqual(count+1, self.number_of_images)
        self.number_of_images -= 1

    def tearDown(self):
        """All images get deleted /api/images/<id>/ through DELETE request"""
        images = Image.objects.all()
        count = images.count

        for img in images:
            url = reverse('images-detail', args=[img.id])
            self.guest_client.delete(url)

        new_count = Image.objects.all().count()
        self.assertNotEqual(new_count, count)
        self.assertEqual(new_count, 0)

