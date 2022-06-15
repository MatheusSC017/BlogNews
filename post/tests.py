from django.shortcuts import reverse
from django.test import Client, TestCase
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from .models import Category, Post, RattingUserPost
from comment.models import Comment
from .views import Blog
from user.views import Login


class BlogPageTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.py_category = Category.objects.create(title_category='Python')
        self.django_category = Category.objects.create(title_category='Django')

        self.post1 = Post.objects.create(title_post='Python Frameworks',
                                         excerpt_post='Conheça os diversos frameworks disponiveis para a linhagem '
                                                      'python',
                                         description_post='Django, Numpy, Pandas, Pytorch, MatPlotLib...',
                                         category_post=self.py_category,
                                         image_post='',
                                         published_date_post='2022-05-21',
                                         ratting_post=3)
        self.post2 = Post.objects.create(title_post='Django',
                                         excerpt_post='Tutorial interativo do framework django',
                                         description_post='Informações diversas sobre o framework e suas '
                                                          'funcionalidades',
                                         category_post=self.django_category,
                                         published_date_post='2022-06-01')
        self.post3 = Post.objects.create(title_post='Python Machine Learning',
                                         excerpt_post='Introdução a tecnicas de ML com python',
                                         description_post='O que é ML e apresentação teorica do seu '
                                                          'funcionamento',
                                         category_post=self.py_category,
                                         published_date_post='2022-01-09',
                                         ratting_post=5)
        self.post4 = Post.objects.create(title_post='Python Machine Learning Frameworks',
                                         excerpt_post='Introdução a tecnicas de ML com python e seus frameworks',
                                         description_post='Framworks Pythons voltados ao uso de Machine Learning',
                                         category_post=self.py_category,
                                         published_date_post='2022-06-04',
                                         ratting_post=4,
                                         published_post=False)
        self.post5 = Post.objects.create(title_post='Python análise de dados',
                                         excerpt_post='Curso de python DataScience (Frameworks)',
                                         description_post='Informações sobre os processos envolvendo análise de dados',
                                         category_post=self.py_category,
                                         published_date_post='2020-01-01',
                                         ratting_post=4,
                                         published_post=True)

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
        return [_.pk for _ in response.context.get('posts')]


class PostPageTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.py_category = Category.objects.create(title_category='Python')

        self.user = User.objects.create_user('username_test', 'test@test.com.br', 'password_test')

        self.post1 = Post.objects.create(title_post='Python Frameworks',
                                         excerpt_post='Conheça os diversos frameworks disponiveis para a linhagem '
                                                      'python',
                                         description_post='Django, Numpy, Pandas, Pytorch, MatPlotLib...',
                                         category_post=self.py_category)
        self.post2 = Post.objects.create(title_post='Python Machine Learning Frameworks',
                                         excerpt_post='Introdução a tecnicas de ML com python e seus frameworks',
                                         description_post='Framworks Pythons voltados ao uso de Machine Learning',
                                         category_post=self.py_category,
                                         published_post=False)
        self.comment = Comment.objects.create(user_comment=self.user,
                                              post_comment=self.post1,
                                              comment='Testando')

    def test_connection_with_the_post_page(self):
        response = self.client.get(reverse('post:post', args=[self.post1.pk]))
        self.assertEqual(response.status_code, 200)

    def test_access_to_unpublished_post(self):
        response = self.client.get(reverse('post:post', args=[self.post2.pk]))
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
                                                 'password': 'password_test', })
        views = self.post1.user_views_post
        response = self.client.get(reverse('post:post', args=[self.post1.pk]))
        self.assertEqual(response.context.get('post').user_views_post, views + 1)

    def test_double_view_post(self):
        response = self.client.get(reverse('post:post', args=[self.post1.pk]))
        views = response.context.get('post').anonymous_views_post
        response = self.client.get(reverse('post:post', args=[self.post1.pk]))
        self.assertEqual(response.context.get('post').anonymous_views_post, views)

    def test_post_method_with_incorrect_action(self):
        user_parameter = {'username': 'username_test', 'password': 'password_test', }
        action_parameter = {'action': 'incorrect-action', }
        self.template_comment_action_with_user_logged_in(user_parameter, action_parameter, 'Ação inválida')

    def test_post_method_with_user_logged_out(self):
        response = self.client.post(reverse('post:post', args=[self.post1.pk]),
                                    {'comment': 'Comment_test',
                                     'action': 'create-comment', })
        self.assertEqual(response.resolver_match.func.__name__, Login.as_view().__name__)

    def test_comment_registration_with_user_logged_in(self):
        user_parameter = {'username': 'username_test', 'password': 'password_test', }
        action_parameter = {'comment': 'Comment_test', 'action': 'create-comment', }
        self.template_comment_action_with_user_logged_in(user_parameter, action_parameter, 'Comentário adicionado')

    def test_comment_update_with_user_logged_in(self):
        user_parameter = {'username': 'username_test', 'password': 'password_test', }
        action_parameter = {'comment': 'Comment_test', 'comment-pk': self.comment.pk, 'action': 'update-comment', }
        self.template_comment_action_with_user_logged_in(user_parameter, action_parameter, 'Comentário editado')

    def test_comment_delete_with_user_logged_in(self):
        user_parameter = {'username': 'username_test', 'password': 'password_test', }
        action_parameter = {'comment-pk': self.comment.pk, 'action': 'delete-comment', }
        self.template_comment_action_with_user_logged_in(user_parameter, action_parameter, 'Comentário deletado')

    def template_comment_action_with_user_logged_in(self, user_parameters, action_parameters, message):
        self.client.post(reverse('user:login'), user_parameters)
        response = self.client.post(reverse('post:post', args=[self.post1.pk]), action_parameters)
        self.assertRedirects(response, reverse('post:post', args=[self.post1.pk]))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 2)
        self.assertEqual(str(messages[1]), message)
