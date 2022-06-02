from django.shortcuts import reverse
from django.test import Client, TestCase
from . import views
from .models import Category, Post, RattingUserPost


class BlogPageTest(TestCase):
    def setUp(self):
        self.client = Client()
        py_category = Category(title_category='Python')
        django_category = Category(title_category='Django')

        Post(title_post='Python Frameworks',
             excerpt_post='Conheça os diversos frameworks disponiveis para a linhagem python',
             description_post='Django, Numpy, Pandas, Pytorch, MatPlotLib...',
             category_post=py_category)
        Post(title_post='Django',
             excerpt_post='Tutorial interativo de django',
             description_post='Informações diversas sobre o framework e suas funcionalidades',
             category_post=django_category)
        Post(title_post='Python Machine Learning',
             excerpt_post='Introdução a tecnicas de ML com python',
             description_post='O que é ML e apresentação teorica do seu funcionamento',
             category_post=py_category)

    def test_connection_with_the_page(self):
        response = self.client.get(reverse('blog:blog'))
        self.assertEqual(response.status_code, 200)

    def test_post_data_receiving(self):
        response = self.client.get(reverse('blog:blog'))
        self.assertIn('posts', response.context)
