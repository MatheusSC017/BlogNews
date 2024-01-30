from django.test import TestCase, Client, override_settings
from django.contrib.auth.models import User, Permission, ContentType
from django.contrib.messages import get_messages
from django.utils import timezone
from django.shortcuts import reverse
from django.conf import settings
from django.http import HttpRequest
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

        self.search1 = models.Search.objects.create(description='Pegunta 1',
                                                    publication_date=timezone.now(),
                                                    finish_date=timezone.now() + timezone.timedelta(days=30),
                                                    user=self.user)
        self.search2 = models.Search.objects.create(description='Pegunta 2',
                                                    publication_date=timezone.now() - timezone.timedelta(
                                                        days=20),
                                                    finish_date=timezone.now() - timezone.timedelta(days=5),
                                                    user=self.other_user)
        self.search3 = models.Search.objects.create(description='Pegunta 3',
                                                    finish_date=timezone.now() + timezone.timedelta(days=5),
                                                    user=self.user,
                                                    published=False)
        self.search4 = models.Search.objects.create(description='Pegunta 4',
                                                    publication_date=timezone.now() + timezone.timedelta(
                                                        days=20),
                                                    finish_date=timezone.now() + timezone.timedelta(days=50),
                                                    user=self.other_user)
        self.option1 = models.Option.objects.create(response='Resposta 1',
                                                    search=self.search1)
        self.option2 = models.Option.objects.create(response='Resposta 2',
                                                    search=self.search1)
        self.option3 = models.Option.objects.create(response='Resposta 1',
                                                    search=self.search2)
        self.option4 = models.Option.objects.create(response='Resposta 2',
                                                    search=self.search2)
        self.option5 = models.Option.objects.create(response='Resposta 1',
                                                    search=self.search3)
        self.option6 = models.Option.objects.create(response='Resposta 2',
                                                    search=self.search3)
        self.option7 = models.Option.objects.create(response='Resposta 1',
                                                    search=self.search4)
        self.option8 = models.Option.objects.create(response='Resposta 2',
                                                    search=self.search4)
        models.VottingUserOption.objects.create(user=self.other_user,
                                                option=self.option2)


class SearchesPageTestCase(SearchTestCase):
    def test_user_search_page_connection_and_context(self):
        response = self.client.get(reverse('search:searches'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.func.__name__, views.Searches.as_view().__name__)
        self.assertIn('searches', response.context)
        self.assertEqual(len(response.context.get('searches')), 2)
        self.assertEqual(response.context.get('searches')[0].get('search').pk, self.search1.pk)
        self.assertEqual(response.context.get('searches')[1].get('search').pk, self.search2.pk)


@override_settings(RECAPTCHA_SITE_KEY=settings.RECAPTCHA_SITE_KEY_TEST,
                   RECAPTCHA_SECRET_KEY=settings.RECAPTCHA_SECRET_KEY_TEST)
class SearchPageTestCase(SearchTestCase):
    def test_search_page_with_inactive_search(self):
        response = self.client.get(reverse('search:search', args=[self.search3.pk, ]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('search:searches'))

    def test_search_page_with_future_search(self):
        response = self.client.get(reverse('search:search', args=[self.search4.pk, ]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('search:searches'))

    def test_search_page_connection_and_context(self):
        response = self.client.get(reverse('search:search', args=[self.search1.pk, ]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.func.__name__, views.Search.as_view().__name__)
        self.assertIn('search', response.context)
        self.assertIn('options', response.context)
        self.assertEqual(len(response.context['options']), 2)
        self.assertIn('max_vote', response.context)
        self.assertIn('status', response.context)

    def test_search_page_vote_with_inactive_search(self):
        self.client.login(username='username_test', password='password_test', request=HttpRequest())
        response = self.client.post(reverse('search:search', args=[self.search3.pk, ]),
                                    {'optionChoice': self.option6.pk})
        self.assertEqual(response.status_code, 404)

    def test_search_page_vote_with_future_search(self):
        self.client.login(username='username_test', password='password_test', request=HttpRequest())
        response = self.client.post(reverse('search:search', args=[self.search4.pk, ]),
                                    {'optionChoice': self.option7.pk})
        self.assertEqual(response.status_code, 404)

    def test_search_page_vote_finished_search(self):
        self.client.login(username='username_test', password='password_test', request=HttpRequest())
        response = self.client.post(reverse('search:search', args=[self.search2.pk, ]),
                                    {'optionChoice': self.option3.pk})
        self.assertEqual(response.status_code, 404)

    def test_search_page_new_vote(self):
        self.client.login(username='username_test', password='password_test', request=HttpRequest())
        response = self.client.post(reverse('search:search', args=[self.search1.pk, ]),
                                    {'optionChoice': self.option1.pk,
                                     'g-recaptcha-response': 'RECAPTCHA', })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('search:search', args=[self.search1.pk, ]))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Obrigado pelo voto')

    def test_search_page_update_vote(self):
        self.client.login(username='username_test2', password='password_test2', request=HttpRequest())
        response = self.client.post(reverse('search:search', args=[self.search1.pk, ]),
                                    {'optionChoice': self.option1.pk,
                                     'g-recaptcha-response': 'RECAPTCHA', })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('search:search', args=[self.search1.pk, ]))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Obrigado pelo voto')


class UserSearchPageTestCase(SearchTestCase):
    def test_user_search_page_without_user(self):
        response = self.client.get(reverse('search:user_search'))
        self.assertEqual(response.status_code, 302)

    def test_user_search_page_with_user_without_permission(self):
        self.client.login(username='username_test3', password='password_test3', request=HttpRequest())
        response = self.client.get(reverse('search:user_search'))
        self.assertEqual(response.status_code, 403)

    def test_user_search_page_connection_and_context(self):
        self.client.login(username='username_test', password='password_test', request=HttpRequest())
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
        self.client.login(username='username_test3', password='password_test3', request=HttpRequest())
        response = self.client.get(reverse('search:search_create'))
        self.assertEqual(response.status_code, 403)

    def test_create_search_page_connection_and_context(self):
        self.client.login(username='username_test', password='password_test', request=HttpRequest())
        response = self.client.get(reverse('search:search_create'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)
        self.assertIn('option_form', response.context)

    def test_create_search(self):
        self.client.login(username='username_test', password='password_test', request=HttpRequest())
        response = self.client.post(reverse('search:search_create'), {
            'description': 'Test Search Description',
            'publication_date': '01/01/2021 12:00:00',
            'finish_date': '01/01/2022 23:59:59',
            'option_set-MIN_NUM_FORMS': '2',
            'option_set-MAX_NUM_FORMS': '8',
            'option_set-TOTAL_FORMS': '2',
            'option_set-INITIAL_FORMS': '0',
            'option_set-0-response': 'Option 1',
            'option_set-1-response': 'Option 2',
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('search:user_search'))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Pesquisa cadastrada')


class UpdateSearchPageTestCase(SearchTestCase):
    def test_update_search_page_connection_without_user(self):
        response = self.client.get(reverse('search:search_update', kwargs={'pk': self.search1.pk, }))
        self.assertEqual(response.status_code, 302)

    def test_update_search_page_connection_with_user_without_permission(self):
        self.client.login(username='username_test3', password='password_test3', request=HttpRequest())
        response = self.client.get(reverse('search:search_update', kwargs={'pk': self.search1.pk, }))
        self.assertEqual(response.status_code, 403)

    def test_update_search_page_with_other_user(self):
        self.client.login(username='username_test2', password='password_test2', request=HttpRequest())
        response = self.client.get(reverse('search:search_update', kwargs={'pk': self.search1.pk, }))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('search:user_search'))

    def test_update_search_page_connection_and_context(self):
        self.client.login(username='username_test', password='password_test', request=HttpRequest())
        response = self.client.get(reverse('search:search_update', kwargs={'pk': self.search1.pk, }))
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)
        self.assertIn('option_form', response.context)

    def test_update_search(self):
        self.client.login(username='username_test', password='password_test', request=HttpRequest())
        response = self.client.post(reverse('search:search_update', kwargs={'pk': self.search1.pk, }), {
            'description': 'Test Search Description',
            'publication_date': '01/01/2021 12:00:00',
            'finish_date': '01/01/2022 23:59:59',
            'option_set-MIN_NUM_FORMS': '2',
            'option_set-MAX_NUM_FORMS': '8',
            'option_set-TOTAL_FORMS': '2',
            'option_set-INITIAL_FORMS': '0',
            'option_set-0-response': 'Option 1',
            'option_set-1-response': 'Option 2',
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('search:user_search'))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Pesquisa atualizada')


class DeleteSearchMethodTestCase(SearchTestCase):
    def test_delete_search_method_get_connection(self):
        self.client.login(username='username_test', password='password_test', request=HttpRequest())
        response = self.client.get(reverse('search:search_delete'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('search:user_search'))

    def test_delete_search_method_connection_without_user(self):
        response = self.client.post(reverse('search:search_delete'), {'primary-key': self.search1.pk, })
        self.assertEqual(response.status_code, 302)

    def test_delete_search_method_connection_with_user_without_permission(self):
        self.client.login(username='username_test3', password='password_test3', request=HttpRequest())
        response = self.client.post(reverse('search:search_delete'), {'primary-key': self.search1.pk, })
        self.assertEqual(response.status_code, 302)

    def test_delete_search_method_with_other_user(self):
        self.client.login(username='username_test2', password='password_test2', request=HttpRequest())
        response = self.client.post(reverse('search:search_delete'), {'primary-key': self.search1.pk, })
        self.assertEqual(response.status_code, 404)

    def test_delete_search(self):
        self.client.login(username='username_test', password='password_test', request=HttpRequest())
        response = self.client.post(reverse('search:search_delete'), {'primary-key': self.search1.pk, })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('search:user_search'))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Pesquisa deletada')
