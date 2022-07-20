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

    user_report = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='usuário')
    status_report = models.CharField(max_length=1, choices=status, default=waiting, verbose_name='situação')
    description_report = models.TextField(verbose_name='descrição')
    creation_date_report = models.DateTimeField(default=tz.now, verbose_name='data de criação')

    def __str__(self):
        return str(self.user_report)

    class Meta:
        verbose_name = 'denúncia'
