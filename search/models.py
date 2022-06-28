from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Search(models.Model):
    description_search = models.TextField(max_length=300, verbose_name='descrição')
    creation_date_search = models.DateTimeField(default=timezone.now, verbose_name='data de criação')
    edition_date_search = models.DateTimeField(default=timezone.now, verbose_name='data de edição')
    publication_date_search = models.DateTimeField(default=timezone.now, verbose_name='data de publicação')
    finish_date_search = models.DateTimeField(verbose_name='data de termino')
    published_search = models.BooleanField(default=True, verbose_name='publicado')
    user_search = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='usuário')

    def __str__(self):
        return self.description_search

    class Meta:
        verbose_name = 'pesquisa'


class Option(models.Model):
    response_option = models.TextField(max_length=300, verbose_name='opção')
    vote_option = models.PositiveIntegerField(verbose_name='número de votos')
    search_option = models.ForeignKey(Search, on_delete=models.CASCADE, verbose_name='pesquisa')

    def __str__(self):
        return self.response_option

    class Meta:
        verbose_name = 'alternativa'
