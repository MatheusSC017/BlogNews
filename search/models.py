from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Search(models.Model):
    description_search = models.TextField(max_length=300, verbose_name='descrição')
    creation_date_search = models.DateTimeField(default=timezone.now(), verbose_name='data de criação')
    edition_date_search = models.DateTimeField(default=timezone.now(), verbose_name='data de edição')
    publication_date_search = models.DateTimeField(default=timezone.now(), verbose_name='data de publicação')
    finish_date_search = models.DateTimeField(default=timezone.now() + timezone.timedelta(days=30),
                                              verbose_name='data de termino')
    published_search = models.BooleanField(default=True, verbose_name='publicado')
    user_search = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='usuário')


class Option(models.Model):
    response_option = models.TextField(max_length=300, verbose_name='opção')
    vote_option = models.PositiveIntegerField(verbose_name='número de votos')
    search_option = models.ForeignKey(Search, on_delete=models.CASCADE, verbose_name='pesquisa')
