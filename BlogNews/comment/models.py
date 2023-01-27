from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from post.models import Post


class Comment(models.Model):
    user_comment = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='usuário')
    post_comment = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='post')
    published_date_comment = models.DateTimeField(default=timezone.now, verbose_name='data de publicação')
    edition_date_comment = models.DateTimeField(default=timezone.now, verbose_name='ultima edição')
    comment = models.TextField(max_length=200, verbose_name='comentário')

    def __str__(self):
        return f'{self.user_comment.first_name} | {self.post_comment.title_post}'

    class Meta:
        verbose_name = 'comentário'
        verbose_name_plural = 'comentários'
