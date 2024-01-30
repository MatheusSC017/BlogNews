from django.db import models
from django.contrib.auth.models import User
from utils.utils import resize_image


class Album(models.Model):
    title = models.CharField(max_length=50, verbose_name='título')
    published = models.BooleanField(default=True, verbose_name='publicar')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='usuário')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'albuns'


def album_direcory_path(instance, filename):
    return f'albuns/album_{instance.album.id}/{filename}'


class Image(models.Model):
    title = models.CharField(max_length=50, blank=True, null=True, verbose_name='título')
    album = models.ForeignKey(Album, on_delete=models.CASCADE, verbose_name='album')
    image = models.ImageField(upload_to=album_direcory_path, verbose_name='imagem')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.image:
            resize_image(self.image, new_width=400)

    class Meta:
        verbose_name = 'imagem'
        verbose_name_plural = 'imagens'
