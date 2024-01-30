from django.test import TestCase, Client
from django.shortcuts import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings
from pathlib import Path
from django.http import HttpRequest
from django.contrib.messages import get_messages
from django.contrib.auth.models import User, Permission, ContentType
from . import models


class AlbumTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        self.user = User.objects.create_user('username_test', 'test@test.com', 'password_test')
        self.user_without_permission = User.objects.create_user('username_test2', 'test@test.com', 'password_test2')

        for model in [models.Album, models.Image]:
            content_type = ContentType.objects.get_for_model(model)
            permissions = Permission.objects.filter(content_type=content_type)
            for permission in permissions:
                self.user.user_permissions.add(permission)

        self.album1 = models.Album.objects.create(title='Album test 1',
                                                  user=self.user)
        self.album2 = models.Album.objects.create(title='Album test 2',
                                                  user=self.user)

        with open(settings.STATICFILES_DIRS[1] / 'album/img/test.jpg', 'rb') as img:
            image = SimpleUploadedFile('image.jpg', img.read())
        self.image1 = models.Image.objects.create(title='Image test 1',
                                                  image=image,
                                                  album=self.album1)
        self.image2 = models.Image.objects.create(title='Image test 2',
                                                  image=image,
                                                  album=self.album1)
        self.image3 = models.Image.objects.create(title='Image test 3',
                                                  image=image,
                                                  album=self.album1)
        self.image4 = models.Image.objects.create(title='Image test 4',
                                                  image=image,
                                                  album=self.album2)


class AlbumPageTestCase(AlbumTestCase):
    def test_album_page_connection_and_context(self):
        response = self.client.get(reverse('album:album'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('albuns', response.context)

    def test_album_page_context_date(self):
        response = self.client.get(reverse('album:album'))
        order = [album.get('album').pk for album in response.context.get('albuns')]
        self.assertEqual([self.album1.pk, ], order)


class ImagePageTestCase(AlbumTestCase):
    def test_image_page_connection_context_and_data(self):
        response = self.client.get(reverse('album:image', args=[self.album1.pk, ]))
        self.assertEqual(response.status_code, 200)
        self.assertIn('album', response.context)
        self.assertIn('images', response.context)
        self.assertEqual(len(response.context.get('images')), 3)


class UserAlbumPageTestCase(AlbumTestCase):
    def test_album_page_without_user(self):
        response = self.client.get(reverse('album:user_album'))
        self.assertEqual(response.status_code, 302)

    def test_album_page_connection_and_context(self):
        self.client.login(username='username_test', password='password_test', request=HttpRequest())
        response = self.client.get(reverse('album:user_album'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('albuns', response.context)

    def test_album_page_connection_with_user_without_permission(self):
        self.client.login(username='username_test2', password='password_test2', request=HttpRequest())
        response = self.client.get(reverse('album:user_album'))
        self.assertEqual(response.status_code, 403)


class AlbumCreatePageTestCase(AlbumTestCase):
    def test_album_create_without_user(self):
        response = self.client.get(reverse('album:album_create'))
        self.assertEqual(response.status_code, 302)

    def test_album_create_page_connection(self):
        self.client.login(username='username_test', password='password_test', request=HttpRequest())
        response = self.client.get(reverse('album:album_create'))
        self.assertEqual(response.status_code, 200)

    def test_album_create_page_connection_with_uset_without_permission(self):
        self.client.login(username='username_test2', password='password_test2', request=HttpRequest())
        response = self.client.get(reverse('album:album_create'))
        self.assertEqual(response.status_code, 403)

    def test_album_create(self):
        self.client.login(username='username_test', password='password_test', request=HttpRequest())
        response = self.client.post(reverse('album:album_create'), {'title': 'Album Test',
                                                                    'published': 'True', })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('album:user_album'))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Álbum cadastrado')


class AlbumUpdateMethodTestCase(AlbumTestCase):
    def test_update_album_without_user(self):
        response = self.client.post(reverse('album:album_update'), {'primary-key': self.album1.pk,
                                                                    'title': 'test Album 2', })
        self.assertEqual(response.status_code, 302)

    def test_update_album_with_user_without_permission(self):
        self.client.login(username='username_test2', password='password_test2', request=HttpRequest())
        response = self.client.post(reverse('album:album_update'), {'primary-key': self.album1.pk,
                                                                    'title': 'test Album 2', })
        self.assertEqual(response.status_code, 302)

    def test_update_album(self):
        self.client.login(username='username_test', password='password_test', request=HttpRequest())
        response = self.client.post(reverse('album:album_update'), {'primary-key': self.album1.pk,
                                                                    'title': 'test Album 2',
                                                                    'published': False, })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('album:user_album'))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Álbum editado')

    def test_update_album_with_invalid_data(self):
        self.client.login(username='username_test', password='password_test', request=HttpRequest())
        response = self.client.post(reverse('album:album_update'), {'primary-key': self.album1.pk,
                                                                    'title': 'test',
                                                                    'published': False, })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('album:user_album'))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Dados incorretos')


class AlbumDeleteMethodTestCase(AlbumTestCase):
    def test_album_delete_without_user(self):
        response = self.client.post(reverse('album:album_delete'), {'primary-key': self.album1.pk, })
        self.assertEqual(response.status_code, 302)

    def test_album_delete_with_user_without_permission(self):
        self.client.login(username='username_test2', password='password_test2', request=HttpRequest())
        response = self.client.post(reverse('album:album_delete'), {'primary-key': self.album1.pk, })
        self.assertEqual(response.status_code, 302)

    def test_album_delete(self):
        self.client.login(username='username_test', password='password_test', request=HttpRequest())
        response = self.client.post(reverse('album:album_delete'), {'primary-key': self.album1.pk, })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('album:user_album'))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Álbum deletado')


class UserImagePageTestCase(AlbumTestCase):
    def test_user_image_page_without_user(self):
        response = self.client.get(reverse('album:user_images', args=[self.album1.pk, ]))
        self.assertEqual(response.status_code, 302)

    def test_user_image_page_with_user_without_permission(self):
        self.client.login(username='username_test2', password='password_test2', request=HttpRequest())
        response = self.client.get(reverse('album:user_images', args=[self.album1.pk, ]))
        self.assertEqual(response.status_code, 403)

    def test_user_image_page_connection_context_and_data(self):
        self.client.login(username='username_test', password='password_test', request=HttpRequest())
        response = self.client.get(reverse('album:user_images', args=[self.album1.pk, ]))
        self.assertEqual(response.status_code, 200)
        self.assertIn('album', response.context)
        self.assertIn('images', response.context)
        self.assertIn('image_form', response.context)
        self.assertEqual(len(response.context.get('images')), 3)


class ImageCreateClassTestCase(AlbumTestCase):
    def test_create_image_class_without_user(self):
        with open(settings.STATICFILES_DIRS[1] / 'album/img/test.jpg', 'rb') as img:
            image = SimpleUploadedFile('image.jpg', img.read())
        response = self.client.post(reverse('album:images_create', args=[self.album1.pk, ]),
                                    {'image_field': [image, ], })
        self.assertEqual(response.status_code, 302)

    def test_create_image_class_with_user_without_permission(self):
        self.client.login(username='username_test2', password='password_test2', request=HttpRequest())
        with open(settings.STATICFILES_DIRS[1] / 'album/img/test.jpg', 'rb') as img:
            image = SimpleUploadedFile('image.jpg', img.read())
        response = self.client.post(reverse('album:images_create', args=[self.album1.pk, ]),
                                    {'image_field': [image, ], })
        self.assertEqual(response.status_code, 403)

    def test_create_image_class(self):
        self.client.login(username='username_test', password='password_test', request=HttpRequest())
        with open(settings.STATICFILES_DIRS[1] / 'album/img/test.jpg', 'rb') as img:
            image = SimpleUploadedFile('image.jpg', img.read())
        response = self.client.post(reverse('album:images_create', args=[self.album1.pk, ]),
                                    {'image_field': [image, ], })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('album:user_images', args=[self.album1.pk, ]))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Imagens cadastradas')


class ImageUpdateMethodTestCase(AlbumTestCase):
    def test_update_image_without_user(self):
        response = self.client.post(reverse('album:image_update', args=[self.album1.pk, ]),
                                    {'primary-key': self.image1.pk,
                                     'title': 'Image title', })
        self.assertEqual(response.status_code, 302)

    def test_update_image_with_user_without_permission(self):
        self.client.login(username='username_test2', password='password_test2', request=HttpRequest())
        response = self.client.post(reverse('album:image_update', args=[self.album1.pk, ]),
                                    {'primary-key': self.image1.pk,
                                     'title': 'Image title', })
        self.assertEqual(response.status_code, 302)

    def test_update_image(self):
        self.client.login(username='username_test', password='password_test', request=HttpRequest())
        response = self.client.post(reverse('album:image_update', args=[self.album1.pk, ]),
                                    {'primary-key': self.image1.pk,
                                     'title': 'Image title', })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('album:user_images', args=[self.album1.pk, ]))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Título editado')

    def test_update_image_with_invalid_data(self):
        self.client.login(username='username_test', password='password_test', request=HttpRequest())
        response = self.client.post(reverse('album:image_update', args=[self.album1.pk, ]),
                                    {'primary-key': self.image1.pk,
                                     'title': 'Test', })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('album:user_images', args=[self.album1.pk, ]))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Título deve possuir ao menos 5 caracteres')


class ImageDeleteMethodTestCase(AlbumTestCase):
    def test_delete_image_without_user(self):
        response = self.client.post(reverse('album:image_delete', args=[self.album1.pk, ]),
                                    {'primary-key': self.image1.pk, })
        self.assertEqual(response.status_code, 302)

    def test_delete_image_with_user_without_permission(self):
        self.client.login(username='username_test2', password='password_test2', request=HttpRequest())
        response = self.client.post(reverse('album:image_delete', args=[self.album1.pk, ]),
                                    {'primary-key': self.image1.pk, })
        self.assertEqual(response.status_code, 302)

    def test_delete_image(self):
        self.client.login(username='username_test', password='password_test', request=HttpRequest())
        response = self.client.post(reverse('album:image_delete', args=[self.album1.pk, ]),
                                    {'primary-key': self.image1.pk, })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('album:user_images', args=[self.album1.pk, ]))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Imagem deletada')


class MultipleImageDeleteMethodTestCase(AlbumTestCase):
    def test_multiple_image_delete_without_user(self):
        response = self.client.post(reverse('album:images_delete', args=[self.album1.pk, ]),
                                    {'delete-items': [self.image1.pk, self.image2.pk, ], })
        self.assertEqual(response.status_code, 302)

    def test_multiple_image_delete_with_user_without_permission(self):
        self.client.login(username='username_test2', password='password_test2', request=HttpRequest())
        response = self.client.post(reverse('album:images_delete', args=[self.album1.pk, ]),
                                    {'delete-items': [self.image1.pk, self.image2.pk, ], })
        self.assertEqual(response.status_code, 302)

    def test_multiple_image_delete(self):
        self.client.login(username='username_test', password='password_test', request=HttpRequest())
        response = self.client.post(reverse('album:images_delete', args=[self.album1.pk, ]),
                                    {'delete-items': [self.image1.pk, self.image2.pk, ], })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('album:user_images', args=[self.album1.pk, ]))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Imagens excluidas')
