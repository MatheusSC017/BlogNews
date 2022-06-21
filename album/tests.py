from django.test import TestCase, Client
from django.shortcuts import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings
from pathlib import Path
from django.contrib.auth.models import User
from . import models


class AlbumPageTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        self.user = User.objects.create_user('username_test', 'test@test.com', 'password_test')

        self.album1 = models.Album.objects.create(title_album='Album test 1',
                                                  user_album=self.user)
        self.album2 = models.Album.objects.create(title_album='Album test 2',
                                                  user_album=self.user)

        with open(settings.MEDIA_ROOT / 'static/test.jpg', 'rb') as img:
            image = SimpleUploadedFile('image.jpg', img.read())
        self.image1 = models.Image.objects.create(title_image='Image test 1',
                                                  image=image,
                                                  album_image=self.album1)
        self.image2 = models.Image.objects.create(title_image='Image test 2',
                                                  image=image,
                                                  album_image=self.album1)
        self.image3 = models.Image.objects.create(title_image='Image test 3',
                                                  image=image,
                                                  album_image=self.album1)
        self.image4 = models.Image.objects.create(title_image='Image test 4',
                                                  image=image,
                                                  album_image=self.album2)

    def test_album_page_connection_and_context(self):
        response = self.client.get(reverse('album:album'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('albuns', response.context)

    def test_album_page_context_date(self):
        response = self.client.get(reverse('album:album'))
        order = [album.get('album').pk for album in response.context.get('albuns')]
        self.assertEqual([self.album1.pk, ], order)


class UserAlbumPageTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        self.user = User.objects.create_user('username_test', 'test@test.com', 'password_test')

    def test_album_page_connection_and_context(self):
        self.client.post(reverse('user:login'), {'username': 'username_test',
                                                 'password': 'password_test', })
        response = self.client.get(reverse('album:user_album'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('albuns', response.context)
