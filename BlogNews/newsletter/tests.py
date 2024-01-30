from django.test import TestCase
from django.contrib.auth.models import User
from django.http import HttpRequest
from django.shortcuts import reverse
from django.contrib.messages import get_messages
from django.utils.crypto import get_random_string
from django.utils import lorem_ipsum
from . import models
from . import views


class NewsLetterUserTestCase(TestCase):
    def setUp(self):
        self.client = self.client_class()

        self.user1 = models.NewsLetterUser.objects.create(email='test1@test.com.br')
        self.user2 = models.NewsLetterUser.objects.create(email='test2@test.com.br',
                                                          activated=False)


class AddUserTestCase(NewsLetterUserTestCase):
    def test_add_user_with_method_get(self):
        response = self.client.get(reverse('newsletter:add_user'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('blog:index'))

    def test_add_user_already_registered_and_activated(self):
        response = self.client.post(reverse('newsletter:add_user'),
                                    {'email-newsletter': 'test1@test.com.br'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('blog:index'))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'E-mail já cadastrado')

    def test_add_user_already_registered_but_not_activated(self):
        response = self.client.post(reverse('newsletter:add_user'),
                                    {'email-newsletter': 'test2@test.com.br'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('newsletter:done_add_user'))

    def test_add_user(self):
        response = self.client.post(reverse('newsletter:add_user'),
                                    {'email-newsletter': 'test@test.com.br'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('newsletter:done_add_user'))


class UnsubscribeTestCase(NewsLetterUserTestCase):
    def test_unsubscribe_connection(self):
        response = self.client.get(reverse('newsletter:unsubscribe'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.func.__name__, views.UnsubscribeNewsletter.as_view().__name__)

    def test_unsubscribe_solicitation(self):
        response = self.client.post(reverse('newsletter:unsubscribe'),
                                    {'email-newsletter': 'test@test.com.br'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('newsletter:unsubscribe_done'))


class ConfirmUnsubscribeTestCase(NewsLetterUserTestCase):
    def generate_session_token(self, email='test@test.com.br'):
        token = get_random_string(length=32)
        session = self.client.session
        session[token] = email
        session.save()
        return token

    def test_confirm_unsubscribe_connection_valid_token(self):
        token = self.generate_session_token()
        response = self.client.get(reverse('newsletter:unsubscribe_confirm', kwargs={'token': token}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.func.__name__, views.ConfirmUnsubscribeNewsletter.as_view().__name__)
        self.assertTrue(response.context['valid_token'])

    def test_confirm_unsubscribe_connection_invalid_token(self):
        token = get_random_string(length=32)
        response = self.client.get(reverse('newsletter:unsubscribe_confirm', kwargs={'token': token}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.func.__name__, views.ConfirmUnsubscribeNewsletter.as_view().__name__)
        self.assertFalse(response.context['valid_token'])

    def test_confirm_unsubscribe_with_email_not_activated(self):
        token = self.generate_session_token(email='test2@test.com.br')
        response = self.client.post(reverse('newsletter:unsubscribe_confirm', kwargs={'token': token}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('blog:index'))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'E-mail não cadastrado')

    def test_confirm_unsubscribe_with_invalid_email(self):
        token = self.generate_session_token(email='test@test.com.br')
        response = self.client.post(reverse('newsletter:unsubscribe_confirm', kwargs={'token': token}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('blog:index'))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'E-mail não cadastrado')

    def test_confirm_unsubscribe(self):
        token = self.generate_session_token(email='test1@test.com.br')
        response = self.client.post(reverse('newsletter:unsubscribe_confirm', kwargs={'token': token}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('newsletter:unsubscribe_finish'))


class SendNewsLetterMessageTestCase(NewsLetterUserTestCase):
    def setUp(self):
        super().setUp()

        self.user = User.objects.create_superuser(username='admin', email='admin@admin.com', password='admin123456')
        self.message = models.NewsLetterMessage.objects.create(title=lorem_ipsum.words(7),
                                                               message=lorem_ipsum.paragraph())

    def test_send_message_for_newsletter_users(self):
        self.client.login(username='admin', password='admin123456', request=HttpRequest())
        response = self.client.post(reverse('admin:newsletter_newslettermessage_changelist'), {
            'action': 'send_newsletter',
            '_selected_action': [self.message.pk, ],
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('admin:newsletter_newslettermessage_changelist'))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), '1 mensagem(ns) enviadas com sucesso.')
        message = models.NewsLetterMessage.objects.get(pk=self.message.pk)
        self.assertTrue(message.published)
