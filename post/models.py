from django.db import models
from django.contrib.auth.models import User
from album.models import Album
from . import types
from utils.utils import resize_image
from datetime import datetime


class Category(models.Model):
    title_category = models.CharField(max_length=50, verbose_name='título')

    def __str__(self):
        return self.title_category

    class Meta:
        verbose_name = 'categoria'
        verbose_name_plural = 'categorias'


class Post(models.Model):
    title_post = models.CharField(max_length=50, verbose_name='título')
    excerpt_post = models.CharField(max_length=300, verbose_name='excerto')
    description_post = models.TextField(verbose_name='descrição')
    image_post = models.ImageField(upload_to='post/%Y/%m/', blank=True, null=True, verbose_name='Imagem')
    ratting_post = models.FloatField(blank=True, null=True, verbose_name='avaliação')
    published_post = models.BooleanField(default=True, verbose_name='publicado')
    published_date_post = models.DateTimeField(default=datetime.now, verbose_name='data de publicação')
    edition_date_post = models.DateTimeField(default=datetime.now, verbose_name='data de edição')
    album_post = models.ForeignKey(Album, blank=True, null=True, on_delete=models.CASCADE, verbose_name='Album')
    category_post = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Categoria')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        resize_image(self.image_post, new_width=600)

    def __str__(self):
        return self.title_post


class RattingUserPost(models.Model):
    user_ratting = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='usuário')
    post_ratting = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='post')
    ratting = types.RattingField(verbose_name='avaliação')

    def __str__(self):
        return f'{self.post_ratting} | {self.user_ratting}'
