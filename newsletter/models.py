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
