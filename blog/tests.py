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

        self.category = model_post.Category.objects.create(title_category='Test')

        self.post1 = model_post.Post.objects.create(title_post='title_test_1',
                                                    excerpt_post='excerpt_test_1',
                                                    description_post='description_test_1',
                                                    published_date_post=tz.now() + tz.timedelta(days=5),
                                                    category_post=self.category,
                                                    user_post=self.user)
        self.post2 = model_post.Post.objects.create(title_post='title_test_2',
                                                    excerpt_post='excerpt_test_2',
                                                    description_post='description_test_2',
                                                    published_post=False,
                                                    category_post=self.category,
                                                    user_post=self.user)
        self.post3 = model_post.Post.objects.create(title_post='title_test_3',
                                                    excerpt_post='excerpt_test_3',
                                                    description_post='description_test_3',
                                                    published_date_post=tz.now() - tz.timedelta(days=10),
                                                    category_post=self.category,
                                                    user_post=self.user)
        self.post4 = model_post.Post.objects.create(title_post='title_test_4',
                                                    excerpt_post='excerpt_test_4',
                                                    description_post='description_test_4',
                                                    published_date_post=tz.now() - tz.timedelta(days=5),
                                                    category_post=self.category,
                                                    user_post=self.user)

        self.album1 = model_album.Album.objects.create(title_album='title_test_1',
                                                       user_album=self.user)
        self.album2 = model_album.Album.objects.create(title_album='title_test_2',
                                                       user_album=self.user,
                                                       published_album=False)

        with open(settings.MEDIA_ROOT / 'static/test.jpg', 'rb') as img:
            self.image = SimpleUploadedFile('image.jpg', img.read())

        self.image1 = model_album.Image.objects.create(image=self.image, album_image=self.album1)
        self.image2 = model_album.Image.objects.create(image=self.image, album_image=self.album1)
        self.image3 = model_album.Image.objects.create(image=self.image, album_image=self.album1)
        self.image4 = model_album.Image.objects.create(image=self.image, album_image=self.album2)
        self.image5 = model_album.Image.objects.create(image=self.image, album_image=self.album2)

        self.search = model_search.Search.objects.create(description_search='description_test',
                                                         finish_date_search=tz.now() + tz.timedelta(days=2),
                                                         user_search=self.user)

        self.option1 = model_search.Option.objects.create(response_option='response_test_1',
                                                          search_option=self.search)
        self.option2 = model_search.Option.objects.create(response_option='response_test_2',
                                                          search_option=self.search)

        self.vote = model_search.VottingUserOption.objects.create(user_votting=self.user,
                                                                  option_votting=self.option2)

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
