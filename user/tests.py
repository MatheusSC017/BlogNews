from django.test import TestCase, Client, override_settings
from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.contrib.messages import get_messages
from blog.views import Home
from .views import Login, Register


@override_settings(RECAPTCHA_SITE_KEY='6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI',
                   RECAPTCHA_SECRET_KEY='6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe')
class RegisterPageTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_connection_with_registration_page(self):
        response = self.client.get(reverse('user:register'))
        self.assertEqual(response.status_code, 200)

    def test_access_registration_page_with_user_already_logged_in(self):
        User.objects.create_user(username='username_test', email='email@test.com', password='password_test')
        self.client.post(reverse('user:login'), {'username': 'username_test',
                                                 'password': 'password_test',
                                                 'g-recaptcha-response': 'recaptcha', })
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
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Usuário cadastrado')

    def registration_test(self, username='username_test', password1='ut123_name_ut', password2='ut123_name_ut'):
        response = self.client.post(reverse('user:register'), {'username': username,
                                                               'first_name': 'username',
                                                               'last_name': 'test',
                                                               'email': 'username@test.com',
                                                               'password1': password1,
                                                               'password2': password2, })
        return response


@override_settings(RECAPTCHA_SITE_KEY='6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI',
                   RECAPTCHA_SECRET_KEY='6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe')
class UpdatePageTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        self.user = User.objects.create_user(username='username_test',
                                             email='email@test.com',
                                             password='password_test')

    def test_connection_with_update_page_without_user(self):
        response = self.client.get(reverse('user:update'))
        self.assertEqual(response.status_code, 302)

    def test_connection_with_update_page(self):
        self.client.post(reverse('user:login'), {'username': 'username_test',
                                                 'password': 'password_test',
                                                 'g-recaptcha-response': 'recaptcha', })
        response = self.client.get(reverse('user:update'))
        self.assertEqual(response.status_code, 200)

    def test_update_user_with_username_already_created(self):
        User.objects.create_user(username='username_test2', email='email@test.com', password='password_test2')
        self.client.post(reverse('user:login'), {'username': 'username_test',
                                                 'password': 'password_test',
                                                 'g-recaptcha-response': 'recaptcha', })
        response = self.update_test(username='username_test2')
        self.assertEqual(response.resolver_match.func.__name__, Register.as_view().__name__)

    def test_update_user(self):
        self.client.post(reverse('user:login'), {'username': 'username_test',
                                                 'password': 'password_test',
                                                 'g-recaptcha-response': 'recaptcha', })
        response = self.update_test()
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('user:update'))
        self.assertTrue(User.objects.get(username='username_test'))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 2)
        self.assertEqual(str(messages[1]), 'Perfil editado')

    def test_update_user_password(self):
        self.client.post(reverse('user:login'), {'username': 'username_test',
                                                 'password': 'password_test',
                                                 'g-recaptcha-response': 'recaptcha', })
        response = self.update_test(password='password_test2',
                                    password_confirm='password_test2')
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 2)
        self.assertEqual(str(messages[1]), 'Perfil editado')

    def update_test(self, username='username_test', password='', password_confirm=''):
        response = self.client.post(reverse('user:update'), {'username': username,
                                                             'first_name': 'username',
                                                             'last_name': 'test',
                                                             'email': 'username@test.com',
                                                             'password1': password,
                                                             'password2': password_confirm})
        return response


@override_settings(RECAPTCHA_SITE_KEY='6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI',
                   RECAPTCHA_SECRET_KEY='6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe')
class LoginPageTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('username_test', 'test@test.com.br', 'password_test')

    def test_connection_with_login_page(self):
        response = self.client.get(reverse('user:login'))
        self.assertEqual(response.status_code, 200)

    def test_login_user_already_logged_in(self):
        self.client.post(reverse('user:login'), data={'username': 'username_test',
                                                      'password': 'password_test',
                                                      'g-recaptcha-response': 'recaptcha', })
        response = self.client.get(reverse('user:login'))
        self.assertEqual(response.resolver_match.func.__name__, Home.as_view().__name__)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 2)
        self.assertEqual(str(messages[1]), 'Usuário já logado')

    def test_login_user_correct_data(self):
        response = self.client.post(reverse('user:login'), data={'username': 'username_test',
                                                                 'password': 'password_test',
                                                                 'g-recaptcha-response': 'recaptcha', })
        self.assertEqual(response.resolver_match.func.__name__, Home.as_view().__name__)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Usuário logado')

    def test_login_user_incorrect_data(self):
        response = self.client.post(reverse('user:login'), data={'username': 'username_test',
                                                                 'password': 'password',
                                                                 'g-recaptcha-response': 'recaptcha', })
        self.assertEqual(response.resolver_match.func.__name__, Login.as_view().__name__)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Usuário ou senha incorretos')


@override_settings(RECAPTCHA_SITE_KEY='6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI',
                   RECAPTCHA_SECRET_KEY='6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe')
class LogoutPageTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('username_test', 'test@test.com.br', 'password_test')

    def test_logout_connection_page(self):
        response = self.client.get(reverse('user:logout'))
        self.assertEqual(response.status_code, 302)

    def test_logout_user_already_logged_out(self):
        response = self.client.get(reverse('user:logout'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('user:login'))

    def test_logout_user(self):
        self.client.post(reverse('user:login'), data={'username': 'username_test',
                                                      'password': 'password_test',
                                                      'g-recaptcha-response': 'recaptcha', })
        response = self.client.get(reverse('user:logout'))
        self.assertRedirects(response, reverse('blog:index'))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 2)
        self.assertEqual(str(messages[1]), 'Usuário deslogado')
