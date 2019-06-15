from django.test import TestCase, Client
from .models import Product
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse


class HomePageTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(username='hkjlklj')
        Product.objects.create(
            title='htyj',
            url='dsfgdsfg',
            pub_date=timezone.now(),

            image=SimpleUploadedFile(name='test_image.jpg', content=b'stroka',
                                     content_type='image/jpeg'),
            icon='icon',
            body='lkjkljhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh',
            hunter=user
        )

    def test_homepage(self):
        client = Client()
        response = client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/home.html')
        self.assertEqual(list(response.context['products']), list(Product.objects.all()))

    def test_detail(self):
        client = Client()
        id1 = Product.objects.first().id
        response = client.get(reverse('detail', kwargs={'product_id': id1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/detail.html')
        self.assertEqual(response.context['product'], Product.objects.get(pk=id1))

        response = client.get(id1 + 1)
        self.assertEqual(response.status_code, 404)
