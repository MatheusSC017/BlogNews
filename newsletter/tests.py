from django.test import TestCase
from django.shortcuts import reverse
from django.contrib.messages import get_messages
from django.utils.crypto import get_random_string
from . import models
from . import views


class NewsLetterUserTestCase(TestCase):
    def setUp(self):
        self.client = self.client_class()

        self.user1 = models.NewsLetterUser.objects.create(email_newsletteruser='test1@test.com.br')
        self.user2 = models.NewsLetterUser.objects.create(email_newsletteruser='test2@test.com.br',
                                                          activated_newsletteruser=False)


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
