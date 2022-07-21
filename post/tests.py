from django.shortcuts import reverse
from django.test import Client, TestCase, override_settings
from django.contrib.auth.models import User, Permission, ContentType
from django.contrib.messages import get_messages
from django.utils import timezone as tz
from django.conf import settings
from .models import Category, Post, RattingUserPost
from comment.models import Comment
from .views import Post as PostView, Blog
from user.views import Login


class BlogTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.py_category = Category.objects.create(title_category='Python')
        self.django_category = Category.objects.create(title_category='Django')

        self.user = User.objects.create_user('username_test', 'test@test.com.br', 'password_test')
        self.other_user = User.objects.create_user('username_test2', 'test@test.com.br', 'password_test2')

        content_type = ContentType.objects.get_for_model(Post)
        permissions = Permission.objects.filter(content_type=content_type)
        for permission in permissions:
            self.user.user_permissions.add(permission)

        self.post1 = Post.objects.create(title_post='Python Frameworks',
                                         excerpt_post='Conheça os diversos frameworks disponiveis para a linhagem '
                                                      'python',
                                         description_post='Django, Numpy, Pandas, Pytorch, MatPlotLib...',
                                         category_post=self.py_category,
                                         publication_date_post=tz.now() - tz.timedelta(days=30),
                                         user_post=self.user)
        self.post2 = Post.objects.create(title_post='Django',
                                         excerpt_post='Tutorial interativo do framework django',
                                         description_post='Informações diversas sobre o framework e suas '
                                                          'funcionalidades',
                                         category_post=self.django_category,
                                         publication_date_post=tz.now() - tz.timedelta(days=20),
                                         user_post=self.user)
        self.post3 = Post.objects.create(title_post='Python Machine Learning',
                                         excerpt_post='Introdução a tecnicas de ML com python',
                                         description_post='O que é ML e apresentação teorica do seu '
                                                          'funcionamento',
                                         category_post=self.py_category,
                                         publication_date_post=tz.now() - tz.timedelta(days=90),
                                         user_post=self.user)
        self.post4 = Post.objects.create(title_post='Python Machine Learning Frameworks',
                                         excerpt_post='Introdução a tecnicas de ML com python e seus frameworks',
                                         description_post='Framworks Pythons voltados ao uso de Machine Learning',
                                         category_post=self.py_category,
                                         publication_date_post=tz.now() - tz.timedelta(days=15),
                                         published_post=False,
                                         user_post=self.user)
        self.post5 = Post.objects.create(title_post='Python análise de dados',
                                         excerpt_post='Curso de python DataScience (Frameworks)',
                                         description_post='Informações sobre os processos envolvendo análise de dados',
                                         category_post=self.py_category,
                                         publication_date_post=tz.now() - tz.timedelta(days=120),
                                         user_post=self.user)
        self.post6 = Post.objects.create(title_post='Posts sobre informação futura',
                                         excerpt_post='Python e o futuro',
                                         description_post='Python e o futuro',
                                         category_post=self.py_category,
                                         publication_date_post=tz.now() + tz.timedelta(days=120),
                                         user_post=self.other_user)

        RattingUserPost.objects.create(user_ratting=self.user,
                                       post_ratting=self.post1,
                                       ratting=3)
        RattingUserPost.objects.create(user_ratting=self.user,
                                       post_ratting=self.post3,
                                       ratting=5)
        RattingUserPost.objects.create(user_ratting=self.user,
                                       post_ratting=self.post4,
                                       ratting=4)
        RattingUserPost.objects.create(user_ratting=self.user,
                                       post_ratting=self.post5,
                                       ratting=4)


class BlogPageTestCase(BlogTestCase):
    def test_connection_with_the_blog_page(self):
        response = self.client.get(reverse('post:blog'))
        self.assertEqual(response.status_code, 200)

    def test_post_data_receiving(self):
        response = self.client.get(reverse('post:blog'))
        self.assertIn('posts', response.context)

    def test_post_data_default_configuration(self):
        self.assertEqual([self.post2.pk, self.post1.pk, self.post3.pk, self.post5.pk], self.template_post_data_order())

    def test_post_data_ordering_by_ratting(self):
        order = self.template_post_data_order({'order_by': 'avaliacao', })
        self.assertEqual([self.post3.pk, self.post5.pk, self.post1.pk, self.post2.pk], order)

    def test_post_data_with_category_select(self):
        order = self.template_post_data_order({'category': str(self.py_category.pk), })
        self.assertEqual([self.post1.pk, self.post3.pk, self.post5.pk], order)

    def test_post_data_with_category_select_and_ordering_by_ratting(self):
        order = self.template_post_data_order({'order_by': 'avaliacao',
                                               'category': str(self.py_category.pk), })
        self.assertEqual([self.post3.pk, self.post5.pk, self.post1.pk], order)

    def test_post_data_search_framework(self):
        order = self.template_post_data_order({'search': 'framework', })
        self.assertEqual([self.post2.pk, self.post1.pk, self.post5.pk], order)

    def test_post_data_search_framework_with_category_select(self):
        order = self.template_post_data_order({'search': 'framework',
                                               'category': str(self.py_category.pk), })
        self.assertEqual([self.post1.pk, self.post5.pk], order)

    def test_post_data_search_framework_and_ordering_by_ratting(self):
        order = self.template_post_data_order({'search': 'framework',
                                               'order_by': 'avaliacao', })
        self.assertEqual([self.post5.pk, self.post1.pk, self.post2.pk], order)

    def test_post_data_search_framework_with_category_select_and_ordering_by_ratting(self):
        order = self.template_post_data_order({'search': 'framework',
                                               'order_by': 'avaliacao',
                                               'category': str(self.py_category.pk), })
        self.assertEqual([self.post5.pk, self.post1.pk], order)

    def template_post_data_order(self, parameter={}):
        response = self.client.get(reverse('post:blog'), parameter)
        return [post.pk for post in response.context.get('posts')]


@override_settings(RECAPTCHA_SITE_KEY=settings.RECAPTCHA_SITE_KEY_TEST,
                   RECAPTCHA_SECRET_KEY=settings.RECAPTCHA_SECRET_KEY_TEST)
class PostPageTestCase(BlogTestCase):
    def test_connection_with_the_post_page(self):
        response = self.client.get(reverse('post:post', args=[self.post1.pk]))
        self.assertEqual(response.status_code, 200)

    def test_access_to_unpublished_post(self):
        response = self.client.get(reverse('post:post', args=[self.post4.pk]))
        self.assertEqual(response.resolver_match.func.__name__, Blog.as_view().__name__)

    def test_receiving_data_post_page(self):
        response = self.client.get(reverse('post:post', args=[self.post1.pk]))
        self.assertIn('post', response.context)
        self.assertIn('comments', response.context)

    def test_view_post(self):
        views = self.post1.anonymous_views_post
        response = self.client.get(reverse('post:post', args=[self.post1.pk]))
        self.assertEqual(response.context.get('post').anonymous_views_post, views + 1)

    def test_view_post_with_logged_in_user(self):
        self.client.post(reverse('user:login'), {'username': 'username_test',
                                                 'password': 'password_test',
                                                 'g-recaptcha-response': 'recaptcha', })
        views = self.post1.user_views_post
        response = self.client.get(reverse('post:post', args=[self.post1.pk]))
        self.assertEqual(response.context.get('post').user_views_post, views + 1)

    def test_double_view_post(self):
        response = self.client.get(reverse('post:post', args=[self.post1.pk]))
        views = response.context.get('post').anonymous_views_post
        response = self.client.get(reverse('post:post', args=[self.post1.pk]))
        self.assertEqual(response.context.get('post').anonymous_views_post, views)

    def test_post_method_with_user_logged_out(self):
        response = self.client.post(reverse('post:post', args=[self.post1.pk]),
                                    {'comment': 'Comment_test',
                                     'action': 'create-comment', })
        self.assertEqual(response.resolver_match.func.__name__, Login.as_view().__name__)

    def test_register_feedback_to_post(self):
        self.client.post(reverse('user:login'), {'username': 'username_test',
                                                 'password': 'password_test',
                                                 'g-recaptcha-response': 'recaptcha', })
        response = self.client.post(reverse('post:post', args=[self.post1.pk, ]),
                                    {'star': '5', })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('post:post', args=[self.post1.pk, ]))
        comments = list(get_messages(response.wsgi_request))
        self.assertEqual(len(comments), 2)
        self.assertEqual(str(comments[1]), 'Obrigado pelo Feedback')

    def test_update_feedback_to_post(self):
        self.client.post(reverse('user:login'), {'username': 'username_test',
                                                 'password': 'password_test',
                                                 'g-recaptcha-response': 'recaptcha', })
        response = self.client.post(reverse('post:post', args=[self.post3.pk, ]),
                                    {'star': '5', })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('post:post', args=[self.post3.pk, ]))
        comments = list(get_messages(response.wsgi_request))
        self.assertEqual(len(comments), 2)
        self.assertEqual(str(comments[1]), 'Obrigado pelo Feedback')


@override_settings(RECAPTCHA_SITE_KEY=settings.RECAPTCHA_SITE_KEY_TEST,
                   RECAPTCHA_SECRET_KEY=settings.RECAPTCHA_SECRET_KEY_TEST)
class UserBlogPageTestCase(BlogTestCase):
    def test_connection_and_context_of_page_with_user_logged_in(self):
        self.client.post(reverse('user:login'), {'username': 'username_test',
                                                 'password': 'password_test',
                                                 'g-recaptcha-response': 'recaptcha', })
        response = self.client.get(reverse('post:user_blog'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('posts', response.context)

    def test_connection_page_with_user_without_permission(self):
        self.client.post(reverse('user:login'), {'username': 'username_test2',
                                                 'password': 'password_test2',
                                                 'g-recaptcha-response': 'recaptcha', })
        response = self.client.get(reverse('post:user_blog'))
        self.assertEqual(response.status_code, 403)

    def test_connection_page_with_user_logged_out(self):
        response = self.client.get(reverse('post:user_blog'))
        self.assertEqual(response.status_code, 302)

    def test_data_received_user_post_page(self):
        self.client.post(reverse('user:login'), {'username': 'username_test',
                                                 'password': 'password_test',
                                                 'g-recaptcha-response': 'recaptcha', })
        response = self.client.get(reverse('post:user_blog'))
        order = [_.pk for _ in response.context.get('posts')]
        self.assertEqual([self.post4.pk,
                          self.post2.pk,
                          self.post1.pk,
                          self.post3.pk,
                          self.post5.pk], order)
        [164, 162, 161, 163, 165]

    def test_unpublish_post(self):
        self.client.post(reverse('user:login'), {'username': 'username_test',
                                                 'password': 'password_test',
                                                 'g-recaptcha-response': 'recaptcha', })
        response = self.client.post(reverse('post:user_blog'), {'primary-key': self.post1.pk, })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('post:user_blog'))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 2)
        self.assertEqual(str(messages[1]), 'Post despublicado')

    def test_publish_post(self):
        self.client.post(reverse('user:login'), {'username': 'username_test',
                                                 'password': 'password_test',
                                                 'g-recaptcha-response': 'recaptcha', })
        response = self.client.post(reverse('post:user_blog'), {'primary-key': self.post4.pk, })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('post:user_blog'))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 2)
        self.assertEqual(str(messages[1]), 'Post publicado')


@override_settings(RECAPTCHA_SITE_KEY=settings.RECAPTCHA_SITE_KEY_TEST,
                   RECAPTCHA_SECRET_KEY=settings.RECAPTCHA_SECRET_KEY_TEST)
class UserCreatePostPageTestCase(BlogTestCase):
    def test_post_create_connection(self):
        self.client.post(reverse('user:login'), {'username': 'username_test',
                                                 'password': 'password_test',
                                                 'g-recaptcha-response': 'recaptcha', })
        response = self.client.get(reverse('post:post_create'))
        self.assertEqual(response.status_code, 200)

    def test_post_create_connection_with_user_without_permission(self):
        self.client.post(reverse('user:login'), {'username': 'username_test2',
                                                 'password': 'password_test2',
                                                 'g-recaptcha-response': 'recaptcha', })
        response = self.client.get(reverse('post:post_create'))
        self.assertEqual(response.status_code, 403)

    def test_post_create_connection_with_user_loggout(self):
        response = self.client.get(reverse('post:post_create'))
        self.assertEqual(response.status_code, 302)

    def test_post_create(self):
        self.client.post(reverse('user:login'), {'username': 'username_test',
                                                 'password': 'password_test',
                                                 'g-recaptcha-response': 'recaptcha', })
        parameters = {'title_post': 'register_test',
                      'excerpt_post': 'register_test_excerpt_post',
                      'description_post': 'register_test_description_post',
                      'category_post': str(self.py_category.pk),
                      'image_post': '', }
        response = self.client.post(reverse('post:post_create'), parameters)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('post:user_blog'))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 2)
        self.assertEqual(str(messages[1]), 'Post adicionado')


@override_settings(RECAPTCHA_SITE_KEY=settings.RECAPTCHA_SITE_KEY_TEST,
                   RECAPTCHA_SECRET_KEY=settings.RECAPTCHA_SECRET_KEY_TEST)
class UserUpdatePostPageTestCase(BlogTestCase):
    def test_post_update_connection(self):
        self.client.post(reverse('user:login'), {'username': 'username_test',
                                                 'password': 'password_test',
                                                 'g-recaptcha-response': 'recaptcha', })
        response = self.client.get(reverse('post:post_update', args=[self.post1.pk, ]))
        self.assertEqual(response.status_code, 200)

    def test_post_update_connection_with_user_without_permission(self):
        self.client.post(reverse('user:login'), {'username': 'username_test2',
                                                 'password': 'password_test2',
                                                 'g-recaptcha-response': 'recaptcha', })
        response = self.client.get(reverse('post:post_update', args=[self.post1.pk, ]))
        self.assertEqual(response.status_code, 403)

    def test_post_update_connection_with_user_loggout(self):
        response = self.client.get(reverse('post:post_update', args=[self.post1.pk, ]))
        self.assertEqual(response.status_code, 302)

    def test_post_update(self):
        self.client.post(reverse('user:login'), {'username': 'username_test',
                                                 'password': 'password_test',
                                                 'g-recaptcha-response': 'recaptcha', })
        parameters = {'title_post': 'update_test',
                      'excerpt_post': 'update_test_excerpt_post',
                      'description_post': 'update_test_description_post',
                      'category_post': str(self.django_category.pk),
                      'image_post': '', }
        response = self.client.post(reverse('post:post_update', args=[self.post1.pk, ]), parameters)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('post:user_blog'))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 2)
        self.assertEqual(str(messages[1]), 'Post atualizado')
