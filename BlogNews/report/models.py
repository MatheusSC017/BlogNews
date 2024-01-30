from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone as tz


class Report(models.Model):
    waiting = 'w'
    approved = 'a'
    rejected = 'r'

    status = [
        ('w', 'Aguardando'),
        ('a', 'Aprovado'),
        ('r', 'Rejeitado'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='usuário')
    status = models.CharField(max_length=1, choices=status, default=waiting, verbose_name='situação')
    description = models.TextField(verbose_name='descrição')
    creation_date = models.DateTimeField(default=tz.now, verbose_name='data de criação')

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name = 'denúncia'
