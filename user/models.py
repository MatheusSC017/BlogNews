from django.db import models
from django.contrib.auth.models import User


class UserReportRegister(models.Model):
    normal = 'n'
    blocked = 'b'
    status = [
        (normal, 'Normal'),
        (blocked, 'Bloqueado'),
    ]

    user_userreportregister = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='usuário')
    reports_userreportregister = models.PositiveIntegerField(default=0, verbose_name='denúncias')
    status_userreportregister = models.CharField(max_length=1, default=normal, choices=status, verbose_name='situação')

    def __str__(self):
        return str(self.user_userreportregister) + ' - ' + str(self.reports_userreportregister)

    class Meta:
        verbose_name = 'denúncias do usuário'
        verbose_name_plural = 'denúncias dos usuários'
