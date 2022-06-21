from django.db import models
from django.contrib.auth.models import User
from utils.utils import resize_image


class Album(models.Model):
    title_album = models.CharField(max_length=50, verbose_name='título')
    published_album = models.BooleanField(default=True, verbose_name='publicar')
    user_album = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='usuário')

    def __str__(self):
        return self.title_album

    class Meta:
        verbose_name_plural = 'albuns'


def album_direcory_path(instance, filename):
    return f'albuns/album_{instance.album_image.id}/{filename}'


class Image(models.Model):
    title_image = models.CharField(max_length=50, blank=True, null=True, verbose_name='título')
    album_image = models.ForeignKey(Album, on_delete=models.CASCADE, verbose_name='album')
    image = models.ImageField(upload_to=album_direcory_path, verbose_name='imagem')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.image:
            resize_image(self.image, new_width=400)

    class Meta:
        verbose_name = 'imagem'
        verbose_name_plural = 'imagens'
