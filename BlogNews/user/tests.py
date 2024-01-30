from django.test import TestCase, Client, override_settings
from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.contrib.messages import get_messages
from django.conf import settings
from django.http import HttpRequest
from blog.views import Home
from .views import Login, Register
from .models import UserReportRegister


class RegisterPageTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_connection_with_registration_page(self):
        response = self.client.get(reverse('user:register'))
        self.assertEqual(response.status_code, 200)

    def test_access_registration_page_with_user_already_logged_in(self):
        User.objects.create_user(username='username_test', email='email@test.com', password='password_test')
        self.client.login(username='username_test', password='password_test', request=HttpRequest())
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
        self.client.login(username='username_test', password='password_test', request=HttpRequest())
        response = self.client.get(reverse('user:update'))
        self.assertEqual(response.status_code, 200)

    def test_update_user_with_username_already_created(self):
        User.objects.create_user(username='username_test2', email='email@test.com', password='password_test2')
        self.client.login(username='username_test2', password='password_test2', request=HttpRequest())
        response = self.update_test(username='username_test2')
        self.assertEqual(response.resolver_match.func.__name__, Register.as_view().__name__)

    def test_update_user(self):
        self.client.login(username='username_test', password='password_test', request=HttpRequest())
        response = self.update_test()
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('user:update'))
        self.assertTrue(User.objects.get(username='username_test'))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Perfil editado')

    def test_update_user_password(self):
        self.client.login(username='username_test', password='password_test', request=HttpRequest())
        response = self.update_test(password='password_test2',
                                    password_confirm='password_test2')
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Perfil editado')

    def update_test(self, username='username_test', password='', password_confirm=''):
        response = self.client.post(reverse('user:update'), {'username': username,
                                                             'first_name': 'username',
                                                             'last_name': 'test',
                                                             'email': 'username@test.com',
                                                             'password1': password,
                                                             'password2': password_confirm})
        return response


@override_settings(RECAPTCHA_SITE_KEY=settings.RECAPTCHA_SITE_KEY_TEST,
                   RECAPTCHA_SECRET_KEY=settings.RECAPTCHA_SECRET_KEY_TEST)
class LoginPageTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('username_test', 'test@test.com.br', 'password_test')

    def test_connection_with_login_page(self):
        response = self.client.get(reverse('user:login'))
        self.assertEqual(response.status_code, 200)

    def test_login_user_already_logged_in(self):
        self.client.login(username='username_test', password='password_test', request=HttpRequest())
        response = self.client.get(reverse('user:login'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('blog:index'))

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
        self.assertFalse(response.wsgi_request.user.is_authenticated)


class LogoutPageTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('username_test', 'test@test.com.br', 'password_test')

    def test_logout_connection_page(self):
        response = self.client.get(reverse('user:logout'))
        self.assertEqual(response.status_code, 200)

    def test_logout_user(self):
        self.client.login(username='username_test', password='password_test', request=HttpRequest())
        response = self.client.get(reverse('user:logout'))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)


class UserReportRegisterActionsTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        self.admin = User.objects.create_superuser(username='admin', email='admin@test.com', password='admin123456')
        self.user1 = User.objects.create_user(username='username_test1',
                                              email='test@test.com',
                                              password='password_test1')
        self.user2 = User.objects.create_user(username='username_test2',
                                              email='test@test.com',
                                              password='password_test2')

        self.userreportregister1 = UserReportRegister.objects.create(user=self.user1)
        self.userreportregister2 = UserReportRegister.objects.create(user=self.user2,
                                                                     reports=3,
                                                                     status='b')

    def test_block_user_content_creation(self):
        self.client.login(username='admin', password='admin123456', request=HttpRequest())
        response = self.client.post(reverse('admin:user_userreportregister_changelist'), {
            'action': 'block_user_permissions',
            '_selected_action': [self.userreportregister1.pk, ],
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('admin:user_userreportregister_changelist'))
        userreportregister = UserReportRegister.objects.get(pk=self.userreportregister1.pk)
        self.assertEqual(userreportregister.status, 'b')

    def test_unlock_user_content_creation(self):
        self.client.login(username='admin', password='admin123456', request=HttpRequest())
        response = self.client.post(reverse('admin:user_userreportregister_changelist'), {
            'action': 'unlock_user_permissions',
            '_selected_action': [self.userreportregister2.pk, ],
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('admin:user_userreportregister_changelist'))
        userreportregister = UserReportRegister.objects.get(pk=self.userreportregister2.pk)
        self.assertEqual(userreportregister.reports, 0)
        self.assertEqual(userreportregister.status, 'n')
