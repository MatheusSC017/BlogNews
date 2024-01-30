from django.test import TestCase, Client
from django.shortcuts import reverse
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from pathlib import Path
from django.utils import timezone as tz
from django.contrib.auth.models import User
from post import models as model_post
from album import models as model_album
from search import models as model_search


class IndexPageTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        self.user = User.objects.create_user('username_test', 'email@test.com', 'password_test')

        self.category = model_post.Category.objects.create(title='Test')

        self.post1 = model_post.Post.objects.create(title='title_test_1',
                                                    excerpt='excerpt_test_1',
                                                    description='description_test_1',
                                                    publication_date=tz.now() + tz.timedelta(days=5),
                                                    category=self.category,
                                                    user=self.user)
        self.post2 = model_post.Post.objects.create(title='title_test_2',
                                                    excerpt='excerpt_test_2',
                                                    description='description_test_2',
                                                    published=False,
                                                    category=self.category,
                                                    user=self.user)
        self.post3 = model_post.Post.objects.create(title='title_test_3',
                                                    excerpt='excerpt_test_3',
                                                    description='description_test_3',
                                                    publication_date=tz.now() - tz.timedelta(days=10),
                                                    category=self.category,
                                                    user=self.user)
        self.post4 = model_post.Post.objects.create(title='title_test_4',
                                                    excerpt='excerpt_test_4',
                                                    description='description_test_4',
                                                    publication_date=tz.now() - tz.timedelta(days=5),
                                                    category=self.category,
                                                    user=self.user)

        self.album1 = model_album.Album.objects.create(title='title_test_1',
                                                       user=self.user)
        self.album2 = model_album.Album.objects.create(title='title_test_2',
                                                       user=self.user,
                                                       published=False)

        with open(settings.STATICFILES_DIRS[2] / 'blog/img/test.jpg', 'rb') as img:
            self.image = SimpleUploadedFile('image.jpg', img.read())

        self.image1 = model_album.Image.objects.create(image=self.image, album=self.album1)
        self.image2 = model_album.Image.objects.create(image=self.image, album=self.album1)
        self.image3 = model_album.Image.objects.create(image=self.image, album=self.album1)
        self.image4 = model_album.Image.objects.create(image=self.image, album=self.album2)
        self.image5 = model_album.Image.objects.create(image=self.image, album=self.album2)

        self.search = model_search.Search.objects.create(description='description_test',
                                                         finish_date=tz.now() + tz.timedelta(days=2),
                                                         user=self.user)

        self.option1 = model_search.Option.objects.create(response='response_test_1',
                                                          search=self.search)
        self.option2 = model_search.Option.objects.create(response='response_test_2',
                                                          search=self.search)

        self.vote = model_search.VottingUserOption.objects.create(user=self.user,
                                                                  option=self.option2)

    def test_index_page_connection_and_context(self):
        response = self.client.get(reverse('blog:index'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('posts', response.context)
        self.assertEqual(len(response.context['posts']), 2)
        self.assertEqual([self.post4.pk, self.post3.pk], [post.pk for post in response.context['posts']])
        self.assertIn('galery', response.context)
        self.assertEqual(len(response.context['galery']), 3)
        self.assertIn('searches', response.context)
        self.assertEqual(len(response.context['searches']), 1)
        self.assertEqual(response.context['searches'][0].pk, self.search.pk)
        self.assertEqual(response.context['searches'][0].max_option, 'response_test_2')
