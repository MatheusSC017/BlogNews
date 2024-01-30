from django.db import models
from django.utils import timezone as tz


class NewsLetterUser(models.Model):
    email = models.EmailField(verbose_name='e-mail', unique=True)
    creation_date = models.DateTimeField(default=tz.now, verbose_name='data de criação')
    activated_date = models.DateTimeField(default=tz.now, verbose_name='data de ativação')
    activated = models.BooleanField(default=True, verbose_name='ativado')

    def save(self, *args, **kwargs):
        if self.activated:
            self.activated_date = tz.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'usuário'


class NewsLetterMessage(models.Model):
    title = models.CharField(max_length=998, verbose_name='título')
    message = models.TextField(verbose_name='mensagem')
    creation_date = models.DateTimeField(default=tz.now, verbose_name='data de criação')
    edition_date = models.DateTimeField(default=tz.now, verbose_name='última edição')
    published = models.BooleanField(default=False, verbose_name='publicado')

    def save(self, *args, **kwargs):
        self.edition_date = tz.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'mensagem'
        verbose_name_plural = 'mensagens'
