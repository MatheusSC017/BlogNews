from django.test import TestCase, Client
from django.contrib.auth.models import User, Permission, ContentType
from django.contrib.messages import get_messages
from django.utils import timezone
from django.shortcuts import reverse
from . import views
from . import models


class SearchTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        self.user = User.objects.create_user('username_test', 'test@test.com', 'password_test')
        self.other_user = User.objects.create_user('username_test2', 'test@test.com', 'password_test2')
        self.user_without_permission = User.objects.create_user('username_test3', 'test@test.com', 'password_test3')

        content_type = ContentType.objects.get_for_model(models.Search)
        search_permissions = Permission.objects.filter(content_type=content_type)
        for permission in search_permissions:
            self.user.user_permissions.add(permission)
            self.other_user.user_permissions.add(permission)

        self.search1 = models.Search.objects.create(description_search='Pegunta 1',
                                                    publication_date_search=timezone.now(),
                                                    finish_date_search=timezone.now() + timezone.timedelta(days=30),
                                                    user_search=self.user)
        self.search2 = models.Search.objects.create(description_search='Pegunta 2',
                                                    publication_date_search=timezone.now() - timezone.timedelta(
                                                        days=20),
                                                    finish_date_search=timezone.now() + timezone.timedelta(days=10),
                                                    user_search=self.other_user)
        self.search3 = models.Search.objects.create(description_search='Pegunta 3',
                                                    finish_date_search=timezone.now() + timezone.timedelta(days=5),
                                                    user_search=self.user,
                                                    published_search=False)
        self.search4 = models.Search.objects.create(description_search='Pegunta 4',
                                                    publication_date_search=timezone.now() + timezone.timedelta(
                                                        days=20),
                                                    finish_date_search=timezone.now() + timezone.timedelta(days=50),
                                                    user_search=self.other_user)
        self.option1 = models.Option.objects.create(response_option='Resposta 1',
                                                    search_option=self.search1)
        self.option2 = models.Option.objects.create(response_option='Resposta 2',
                                                    search_option=self.search1)
        self.option3 = models.Option.objects.create(response_option='Resposta 1',
                                                    search_option=self.search2)
        self.option4 = models.Option.objects.create(response_option='Resposta 2',
                                                    search_option=self.search2)
        self.option5 = models.Option.objects.create(response_option='Resposta 1',
                                                    search_option=self.search3)
        self.option6 = models.Option.objects.create(response_option='Resposta 2',
                                                    search_option=self.search3)
        self.option7 = models.Option.objects.create(response_option='Resposta 1',
                                                    search_option=self.search4)
        self.option8 = models.Option.objects.create(response_option='Resposta 2',
                                                    search_option=self.search4)


class SearchPageTestCase(SearchTestCase):
    def test_user_search_page_connection_and_context(self):
        response = self.client.get(reverse('search:search'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.func.__name__, views.Searches.as_view().__name__)
        self.assertIn('searches', response.context)
        self.assertEqual(len(response.context.get('searches')), 2)
        self.assertEqual(response.context.get('searches')[0].get('search').pk, self.search1.pk)
        self.assertEqual(response.context.get('searches')[1].get('search').pk, self.search2.pk)


class UserSearchPageTestCase(SearchTestCase):
    def test_user_search_page_without_user(self):
        response = self.client.get(reverse('search:user_search'))
        self.assertEqual(response.status_code, 302)

    def test_user_search_page_with_user_without_permission(self):
        self.client.post(reverse('user:login'), {'username': 'username_test3',
                                                 'password': 'password_test3', })
        response = self.client.get(reverse('search:user_search'))
        self.assertEqual(response.status_code, 403)

    def test_user_search_page_connection_and_context(self):
        self.client.post(reverse('user:login'), {'username': 'username_test',
                                                 'password': 'password_test', })
        response = self.client.get(reverse('search:user_search'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.func.__name__, views.UserSearches.as_view().__name__)
        self.assertIn('searches', response.context)
        self.assertEqual(len(response.context.get('searches')), 2)


class CreateSearchPageTestCase(SearchTestCase):
    def test_create_search_page_connection_without_user(self):
        response = self.client.get(reverse('search:search_create'))
        self.assertEqual(response.status_code, 302)

    def test_create_search_page_connection_with_user_without_permission(self):
        self.client.post(reverse('user:login'), {'username': 'username_test3',
                                                 'password': 'password_test3', })
        response = self.client.get(reverse('search:search_create'))
        self.assertEqual(response.status_code, 403)

    def test_create_search_page_connection_and_context(self):
        self.client.post(reverse('user:login'), {'username': 'username_test',
                                                 'password': 'password_test', })
        response = self.client.get(reverse('search:search_create'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)
        self.assertIn('option_form', response.context)

    def test_create_search(self):
        self.client.post(reverse('user:login'), {'username': 'username_test',
                                                 'password': 'password_test', })
        response = self.client.post(reverse('search:search_create'),
                                    {
                                        'description_search': 'Test Search Description',
                                        'publication_date_search': '01/01/2021 12:00:00',
                                        'finish_date_search': '01/01/2022 23:59:59',
                                        'option_set-MIN_NUM_FORMS': '2',
                                        'option_set-MAX_NUM_FORMS': '8',
                                        'option_set-TOTAL_FORMS': '2',
                                        'option_set-INITIAL_FORMS': '0',
                                        'option_set-0-response_option': 'Option 1',
                                        'option_set-1-response_option': 'Option 2',
                                    })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('search:user_search'))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 2)
        self.assertEqual(str(messages[1]), 'Pesquisa cadastrada')


class UpdateSearchPageTestCase(SearchTestCase):
    def test_update_search_page_connection_without_user(self):
        response = self.client.get(reverse('search:search_update', kwargs={'pk': self.search1.pk, }))
        self.assertEqual(response.status_code, 302)

    def test_update_search_page_connection_with_user_without_permission(self):
        self.client.post(reverse('user:login'), {'username': 'username_test3',
                                                 'password': 'password_test3', })
        response = self.client.get(reverse('search:search_update', kwargs={'pk': self.search1.pk, }))
        self.assertEqual(response.status_code, 403)

    def test_update_search_page_with_other_user(self):
        self.client.post(reverse('user:login'), {'username': 'username_test2',
                                                 'password': 'password_test2', })
        response = self.client.get(reverse('search:search_update', kwargs={'pk': self.search1.pk, }))
        self.assertEqual(response.status_code, 404)

    def test_update_search_page_connection_and_context(self):
        self.client.post(reverse('user:login'), {'username': 'username_test',
                                                 'password': 'password_test', })
        response = self.client.get(reverse('search:search_update', kwargs={'pk': self.search1.pk, }))
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)
        self.assertIn('option_form', response.context)

    def test_update_search(self):
        self.client.post(reverse('user:login'), {'username': 'username_test',
                                                 'password': 'password_test', })
        response = self.client.post(reverse('search:search_update', kwargs={'pk': self.search1.pk, }),
                                    {
                                        'description_search': 'Test Search Description',
                                        'publication_date_search': '01/01/2021 12:00:00',
                                        'finish_date_search': '01/01/2022 23:59:59',
                                        'option_set-MIN_NUM_FORMS': '2',
                                        'option_set-MAX_NUM_FORMS': '8',
                                        'option_set-TOTAL_FORMS': '2',
                                        'option_set-INITIAL_FORMS': '0',
                                        'option_set-0-response_option': 'Option 1',
                                        'option_set-1-response_option': 'Option 2',
                                    })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('search:user_search'))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 2)
        self.assertEqual(str(messages[1]), 'Pesquisa atualizada')


class DeleteSearchMethodTestCase(SearchTestCase):
    def test_delete_search_method_get_connection(self):
        self.client.post(reverse('user:login'), {'username': 'username_test',
                                                 'password': 'password_test', })
        response = self.client.get(reverse('search:search_delete'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('search:user_search'))

    def test_delete_search_method_connection_without_user(self):
        response = self.client.post(reverse('search:search_delete'), {'primary-key': self.search1.pk, })
        self.assertEqual(response.status_code, 302)

    def test_delete_search_method_connection_with_user_without_permission(self):
        self.client.post(reverse('user:login'), {'username': 'username_test3',
                                                 'password': 'password_test3', })
        response = self.client.post(reverse('search:search_delete'), {'primary-key': self.search1.pk, })
        self.assertEqual(response.status_code, 302)

    def test_delete_search_method_with_other_user(self):
        self.client.post(reverse('user:login'), {'username': 'username_test2',
                                                 'password': 'password_test2', })
        response = self.client.post(reverse('search:search_delete'), {'primary-key': self.search1.pk, })
        self.assertEqual(response.status_code, 404)

    def test_delete_search(self):
        self.client.post(reverse('user:login'), {'username': 'username_test',
                                                 'password': 'password_test', })
        response = self.client.post(reverse('search:search_delete'), {'primary-key': self.search1.pk, })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('search:user_search'))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 2)
        self.assertEqual(str(messages[1]), 'Pesquisa deletada')
