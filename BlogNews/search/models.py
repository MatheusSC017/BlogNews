from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Search(models.Model):
    description = models.TextField(max_length=300, verbose_name='descrição')
    creation_date = models.DateTimeField(default=timezone.now, verbose_name='data de criação')
    edition_date = models.DateTimeField(default=timezone.now, verbose_name='data de edição')
    publication_date = models.DateTimeField(default=timezone.now, verbose_name='data de publicação')
    finish_date = models.DateTimeField(verbose_name='data de termino')
    published = models.BooleanField(default=True, verbose_name='publicado')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='usuário')

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = 'pesquisa'


class Option(models.Model):
    response = models.CharField(max_length=300, verbose_name='opção')
    search = models.ForeignKey(Search, on_delete=models.CASCADE, verbose_name='pesquisa')

    def __str__(self):
        return self.response

    class Meta:
        verbose_name = 'alternativa'


class VottingUserOption(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='usuário')
    option = models.ForeignKey(Option, on_delete=models.CASCADE, verbose_name='alternativa')

    class Meta:
        verbose_name = 'voto'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'option', ], name='user_option_vote'
            )
        ]

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name + ' - ' + str(self.option.search.description)
