from django.db import models
from django.utils import timezone as tz


class NewsLetterUser(models.Model):
    email_newsletteruser = models.EmailField(verbose_name='e-mail', unique=True)
    creation_date_newsletteruser = models.DateTimeField(default=tz.now(), verbose_name='data de criação')
    activated_date_newsletteruser = models.DateTimeField(default=tz.now(), verbose_name='data de ativação')
    activated_newsletteruser = models.BooleanField(default=True, verbose_name='ativado')

    def __str__(self):
        return self.email_newsletteruser

    class Meta:
        verbose_name = 'usuário'


class NewsLetterMessage(models.Model):
    title_newslettermessage = models.CharField(max_length=998, verbose_name='título')
    message_newslettermessage = models.TextField(verbose_name='mensagem')
    creation_date_newslettermessage = models.DateTimeField(default=tz.now(), verbose_name='data de criação')
    edition_date_newslettermessage = models.DateTimeField(default=tz.now(), verbose_name='última edição')
    published_newslettermessage = models.BooleanField(default=False, verbose_name='publicado')

    def save(self, *args, **kwargs):
        self.edition_date_newslettermessage = tz.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title_newslettermessage

    class Meta:
        verbose_name = 'mensagem'
        verbose_name_plural = 'mensagens'
