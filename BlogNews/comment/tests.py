from django.shortcuts import reverse
from django.test import TestCase, Client, override_settings
from django.contrib.auth.models import User
from django.utils import timezone as tz
from django.contrib.messages import get_messages
from django.conf import settings
from post.models import Post, Category
from django.http import HttpRequest
from .models import Comment


class CommentTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        self.user = User.objects.create_user('username_test', 'test@test.com.br', 'password_test')
        self.other_user = User.objects.create_user('username_test2', 'test@test.com.br', 'password_test2')

        self.category = Category.objects.create(title='Category Test')

        self.post1 = Post.objects.create(title='Test Title Post 1',
                                         excerpt='Excerpt of the Post',
                                         description='Description of the Post',
                                         category=self.category,
                                         publication_date=tz.now() - tz.timedelta(days=30),
                                         user=self.user)
        self.post2 = Post.objects.create(title='Test Title Post 2',
                                         excerpt='Excerpt of the Post',
                                         description='Description of the Post',
                                         category=self.category,
                                         publication_date=tz.now() + tz.timedelta(days=30),
                                         user=self.user)
        self.post3 = Post.objects.create(title='Test Title Post 3',
                                         excerpt='Excerpt of the Post',
                                         description='Description of the Post',
                                         category=self.category,
                                         published=False,
                                         user=self.user)
        self.post4 = Post.objects.create(title='Test Title Post 4',
                                         excerpt='Excerpt of the Post',
                                         description='Description of the Post',
                                         category=self.category,
                                         publication_date=tz.now() - tz.timedelta(days=30),
                                         user=self.user)

        self.comment1 = Comment.objects.create(user=self.user,
                                               post=self.post1,
                                               comment='Testando')
        self.comment2 = Comment.objects.create(user=self.user,
                                               post=self.post2,
                                               comment='Testando')
        self.comment3 = Comment.objects.create(user=self.user,
                                               post=self.post3,
                                               comment='Testando')


@override_settings(RECAPTCHA_SITE_KEY=settings.RECAPTCHA_SITE_KEY_TEST,
                   RECAPTCHA_SECRET_KEY=settings.RECAPTCHA_SECRET_KEY_TEST)
class CommentCreateMethodTestCase(CommentTestCase):
    def test_create_comment_get_method(self):
        self.client.login(username='username_test', password='password_test', request=HttpRequest())
        response = self.client.get(reverse('comment:comment_create', args=[self.post1.pk, ]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('post:post', args=[self.post1.pk, ]))

    def test_create_comment_without_user(self):
        response = self.client.post(reverse('comment:comment_create', args=[self.post1.pk, ]),
                                    {'comment': 'Comment_test', 'g-recaptcha-response': 'recaptcha', })
        self.assertEqual(response.status_code, 302)

    def test_create_comment_with_unpublished_post(self):
        self.client.login(username='username_test', password='password_test', request=HttpRequest())
        response = self.client.post(reverse('comment:comment_create', args=[self.post3.pk, ]),
                                    {'comment': 'Comment_test', 'g-recaptcha-response': 'recaptcha', })
        self.assertEqual(response.status_code, 404)

    def test_create_comment_post_with_future_publication_date(self):
        self.client.login(username='username_test', password='password_test', request=HttpRequest())
        response = self.client.post(reverse('comment:comment_create', args=[self.post2.pk, ]),
                                    {'comment': 'Comment_test', 'g-recaptcha-response': 'recaptcha', })
        self.assertEqual(response.status_code, 404)

    def test_create_comment(self):
        self.client.login(username='username_test', password='password_test', request=HttpRequest())
        response = self.client.post(reverse('comment:comment_create', args=[self.post1.pk, ]),
                                    {'comment': 'Comment_test', 'g-recaptcha-response': 'recaptcha', })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('post:post', args=[self.post1.pk, ]))
        comments = list(get_messages(response.wsgi_request))
        self.assertEqual(len(comments), 1)
        self.assertEqual(str(comments[0]), 'Comentário adicionado')


class CommentUpdateMethodTestCase(CommentTestCase):
    def test_update_comment_get_method(self):
        self.client.login(username='username_test', password='password_test', request=HttpRequest())
        response = self.client.get(reverse('comment:comment_update', args=[self.post1.pk, ]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('post:post', args=[self.post1.pk, ]))

    def test_update_comment_without_user(self):
        response = self.client.post(reverse('comment:comment_update', args=[self.post1.pk, ]),
                                    {'comment': 'Comment_test', 'primary-key': self.comment1.pk, })
        self.assertEqual(response.status_code, 302)

    def test_update_comment_with_unpublished_post(self):
        self.client.login(username='username_test', password='password_test', request=HttpRequest())
        response = self.client.post(reverse('comment:comment_update', args=[self.post3.pk, ]),
                                    {'comment': 'Comment_test', 'primary-key': self.comment3.pk, })
        self.assertEqual(response.status_code, 404)

    def test_update_comment_post_with_future_publication_date(self):
        self.client.login(username='username_test', password='password_test', request=HttpRequest())
        response = self.client.post(reverse('comment:comment_update', args=[self.post2.pk, ]),
                                    {'comment': 'Comment_test', 'primary-key': self.comment2.pk, })
        self.assertEqual(response.status_code, 404)

    def test_update_comment_with_other_user(self):
        self.client.login(username='username_test2', password='password_test2', request=HttpRequest())
        response = self.client.post(reverse('comment:comment_update', args=[self.post1.pk, ]),
                                    {'comment': 'Comment_test', 'primary-key': self.comment1.pk, })
        self.assertEqual(response.status_code, 404)

    def test_update_comment_with_other_post(self):
        self.client.login(username='username_test', password='password_test', request=HttpRequest())
        response = self.client.post(reverse('comment:comment_update', args=[self.post4.pk, ]),
                                    {'comment': 'Comment_test', 'primary-key': self.comment1.pk, })
        self.assertEqual(response.status_code, 404)

    def test_update_comment(self):
        self.client.login(username='username_test', password='password_test', request=HttpRequest())
        response = self.client.post(reverse('comment:comment_update', args=[self.post1.pk, ]),
                                    {'comment': 'Comment_test', 'primary-key': self.comment1.pk, })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('post:post', args=[self.post1.pk, ]))
        comments = list(get_messages(response.wsgi_request))
        self.assertEqual(len(comments), 1)
        self.assertEqual(str(comments[0]), 'Comentário editado')


class CommentDeleteMethodTestCase(CommentTestCase):
    def test_delete_comment_get_method(self):
        self.client.login(username='username_test', password='password_test', request=HttpRequest())
        response = self.client.get(reverse('comment:comment_delete', args=[self.post1.pk, ]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('post:post', args=[self.post1.pk, ]))

    def test_delete_comment_without_user(self):
        response = self.client.post(reverse('comment:comment_delete', args=[self.post1.pk, ]),
                                    {'primary-key': self.comment1.pk, })
        self.assertEqual(response.status_code, 302)

    def test_delete_comment_with_unpublished_post(self):
        self.client.login(username='username_test', password='password_test', request=HttpRequest())
        response = self.client.post(reverse('comment:comment_delete', args=[self.post3.pk, ]),
                                    {'primary-key': self.comment3.pk, })
        self.assertEqual(response.status_code, 404)

    def test_delete_comment_post_with_future_publication_date(self):
        self.client.login(username='username_test', password='password_test', request=HttpRequest())
        response = self.client.post(reverse('comment:comment_delete', args=[self.post2.pk, ]),
                                    {'primary-key': self.comment2.pk, })
        self.assertEqual(response.status_code, 404)

    def test_delete_comment_with_other_user(self):
        self.client.login(username='username_test2', password='password_test2', request=HttpRequest())
        response = self.client.post(reverse('comment:comment_delete', args=[self.post1.pk, ]),
                                    {'primary-key': self.comment1.pk, })
        self.assertEqual(response.status_code, 404)

    def test_delete_comment_with_other_post(self):
        self.client.login(username='username_test', password='password_test', request=HttpRequest())
        response = self.client.post(reverse('comment:comment_delete', args=[self.post4.pk, ]),
                                    {'primary-key': self.comment1.pk, })
        self.assertEqual(response.status_code, 404)

    def test_delete_comment(self):
        self.client.login(username='username_test', password='password_test', request=HttpRequest())
        response = self.client.post(reverse('comment:comment_delete', args=[self.post1.pk, ]),
                                    {'comment': 'Comment_test', 'primary-key': self.comment1.pk, })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('post:post', args=[self.post1.pk, ]))
        comments = list(get_messages(response.wsgi_request))
        self.assertEqual(len(comments), 1)
        self.assertEqual(str(comments[0]), 'Comentário deletado')
