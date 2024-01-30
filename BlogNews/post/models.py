from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from album.models import Album
from . import types
from utils.utils import resize_image


class Category(models.Model):
    title = models.CharField(max_length=50, verbose_name='título')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'categoria'
        verbose_name_plural = 'categorias'


class Post(models.Model):
    title = models.CharField(max_length=50, verbose_name='título')
    excerpt = models.TextField(max_length=300, verbose_name='excerto')
    description = models.TextField(verbose_name='descrição')
    image = models.ImageField(upload_to='post/%Y/%m/', blank=True, null=True, verbose_name='Imagem')
    anonymous_views = models.PositiveIntegerField(default=0, verbose_name='Visualizações')
    user_views = models.PositiveIntegerField(default=0, verbose_name='Visualizações')
    published = models.BooleanField(default=True, verbose_name='publicado')
    publication_date = models.DateTimeField(default=timezone.now, verbose_name='data de publicação')
    edition_date = models.DateTimeField(default=timezone.now, verbose_name='data de edição')
    album = models.ForeignKey(Album, blank=True, null=True, on_delete=models.CASCADE, verbose_name='Album')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Categoria')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Usuário')

    def save(self, *args, **kwargs):
        self.edition_date = timezone.now()

        super().save(*args, **kwargs)

        if self.image:
            resize_image(self.image, new_width=600)

    def __str__(self):
        return self.title

    def views(self):
        return self.user_views + self.anonymous_views


class RattingUserPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='usuário')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='post')
    ratting = types.RattingField(verbose_name='avaliação')

    class Meta:
        verbose_name = 'avaliação'
        verbose_name_plural = 'avaliações'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'post'], name='ratting_user'
            )
        ]

    def __str__(self):
        return f'{self.post} | {self.user}'
