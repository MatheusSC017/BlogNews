from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.shortcuts import reverse
from blog.views import Home
from .views import Login, Register


class RegisterPageTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_connection_with_registration_page(self):
        response = self.client.get(reverse('user:register'))
        self.assertEqual(response.status_code, 200)

    def test_access_registration_page_with_user_already_logged_in(self):
        response = self.client.get(reverse('user:register'))
        self.assertEqual(response.resolver_match.func.__name__, Home.as_view().__name__)

    def test_registration_user_with_common_password(self):
        response = self.registration_test(password1='username_test', password2='username_test')
        self.assertEqual(response.resolver_match.func.__name__, Register.as_view().__name__)
        self.assertFalse(User.objects.filter(username='username_test'))

    def test_registration_user_with_different_password(self):
        response = self.registration_test(password2='password_test')
        self.assertEqual(response.resolver_match.func.__name__, Register.as_view().__name__)
        self.assertFalse(User.objects.filter(username='username_test'))

    def test_registration_user_with_wrong_username(self):
        response = self.registration_test(username='username_test*')
        self.assertEqual(response.resolver_match.func.__name__, Register.as_view().__name__)
        self.assertFalse(User.objects.filter(username='username_test*'))

    def test_registration_user_with_username_already_created(self):
        User.objects.create_user(username='username_test', email='email@test.com', password='password_test')
        response = self.registration_test()
        self.assertEqual(response.resolver_match.func.__name__, Register.as_view().__name__)

    def test_registration_user(self):
        response = self.registration_test()
        self.assertEqual(response.resolver_match.func.__name__, Home.as_view().__name__)
        self.assertTrue(User.objects.get(username='username_test'))

    def registration_test(self, username='username_test', password1='ut123_name_ut', password2='ut123_name_ut'):
        response = self.client.post(reverse('user:register'), {'username': username,
                                                               'first_name': 'username',
                                                               'last_name': 'test',
                                                               'email': 'username@test.com',
                                                               'password1': password1,
                                                               'password2': password2})
        return response


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
        self.assertRedirects(response, reverse('blog:index'))
