from django.test import TestCase, Client
from django.shortcuts import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings
from pathlib import Path
from django.contrib.messages import get_messages
from django.contrib.auth.models import User, Permission, ContentType
from . import models
from . import views


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
        self.user_without_permission = User.objects.create_user('username_test2', 'test@test.com', 'password_test2')

        content_type = ContentType.objects.get_for_model(models.Album)
        album_permissions = Permission.objects.filter(content_type=content_type)
        for permission in album_permissions:
            self.user.user_permissions.add(permission)

    def test_album_page_connection_and_context(self):
        self.client.post(reverse('user:login'), {'username': 'username_test',
                                                 'password': 'password_test', })
        response = self.client.get(reverse('album:user_album'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('albuns', response.context)

    def test_album_page_connection_with_user_without_permission(self):
        self.client.post(reverse('user:login'), {'username': 'username_test2',
                                                 'password': 'password_test2', })
        response = self.client.get(reverse('album:user_album'))
        self.assertEqual(response.status_code, 403)


class AlbumCreatePageTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        self.user = User.objects.create_user('username_test', 'test@test.com', 'password_test')
        self.user_without_permission = User.objects.create_user('username_test2', 'test@test.com', 'password_test2')

        content_type = ContentType.objects.get_for_model(models.Album)
        album_permissions = Permission.objects.filter(content_type=content_type)
        for permission in album_permissions:
            self.user.user_permissions.add(permission)

    def test_album_create_page_connection(self):
        self.client.post(reverse('user:login'), {'username': 'username_test',
                                                 'password': 'password_test', })
        response = self.client.get(reverse('album:album_create'))
        self.assertEqual(response.status_code, 200)

    def test_album_create_page_connection_with_uset_without_permission(self):
        self.client.post(reverse('user:login'), {'username': 'username_test2',
                                                 'password': 'password_test2', })
        response = self.client.get(reverse('album:album_create'))
        self.assertEqual(response.status_code, 403)

    def test_album_create(self):
        self.client.post(reverse('user:login'), {'username': 'username_test',
                                                 'password': 'password_test', })
        response = self.client.post(reverse('album:album_create'), {'title_album': 'Album Test',
                                                                    'published_album': 'True', })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('album:user_album'))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 2)
        self.assertEqual(str(messages[1]), 'Álbum cadastrado')

    def test_album_create_with_invalid_data(self):
        self.client.post(reverse('user:login'), {'username': 'username_test',
                                                 'password': 'password_test', })
        response = self.client.post(reverse('album:album_create'), {'title_album': 'Test',
                                                                    'published_album': 'False', })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.func.__name__, views.AlbumUser.as_view().__name__)
