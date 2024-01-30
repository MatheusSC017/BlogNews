from django.db import models
from django.contrib.auth.models import User


class UserReportRegister(models.Model):
    normal = 'n'
    blocked = 'b'
    status = [
        (normal, 'Normal'),
        (blocked, 'Bloqueado'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='usuário')
    reports = models.PositiveIntegerField(default=0, verbose_name='denúncias')
    status = models.CharField(max_length=1, default=normal, choices=status, verbose_name='situação')

    def __str__(self):
        return str(self.user) + ' - ' + str(self.reports)

    class Meta:
        verbose_name = 'denúncias do usuário'
        verbose_name_plural = 'denúncias dos usuários'
