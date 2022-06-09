from django.test import TestCase, Client, RequestFactory
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.shortcuts import reverse
from .views import Home, Login

"""
class RegisterPageTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_connection_with_register_page(self):
        response = self.client.get(reverse('user:register'))
        self.assertEqual(response.status_code, 200)
"""

class LoginPageTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('username_test', 'test@test.com.br', 'password_test')

    def test_connection_with_login_page(self):
        response = self.client.get(reverse('user:login'))
        self.assertEqual(response.status_code, 200)

    def test_login_user_already_logged_in(self):
        self.client.post(reverse('user:login'), data={'username': 'username_test',
                                                      'password': 'password_test', })
        response = self.client.get(reverse('user:login'))
        self.assertEqual(response.resolver_match.func.__name__, Home.as_view().__name__)

    def test_login_user_correct_data(self):
        response = self.client.post(reverse('user:login'), data={'username': 'username_test',
                                                                 'password': 'password_test', })
        self.assertEqual(response.resolver_match.func.__name__, Home.as_view().__name__)

    def test_login_user_incorrect_data(self):
        response = self.client.post(reverse('user:login'), data={'username': 'username_test',
                                                                 'password': 'password', })
        self.assertEqual(response.resolver_match.func.__name__, Login.as_view().__name__)


class LogoutPageTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('username_test', 'test@test.com.br', 'password_test')

    def test_logout_connection_page(self):
        response = self.client.get(reverse('user:logout'))
        self.assertEqual(response.status_code, 302)

    def test_logout_user_already_logged_out(self):
        response = self.client.get(reverse('user:logout'))
        self.assertRedirects(response, reverse('user:login'))

    def test_logout_user(self):
        self.client.post(reverse('user:login'), data={'username': 'username_test',
                                                      'password': 'password_test', })
        response = self.client.get(reverse('user:logout'))
        self.assertRedirects(response, reverse('user:index'))
        self.assertEqual(self.user.is_authenticated, False)
