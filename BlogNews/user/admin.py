from django.contrib import admin
from django.contrib.auth.models import ContentType, Permission
from post.models import Post
from search.models import Search, Option
from album.models import Album, Image
from .models import UserReportRegister


class UserReportRegisterAdmin(admin.ModelAdmin):
    list_display = ['user', 'reports', 'status', ]
    list_display_links = ['user', ]
    list_filter = ['status', ]
    search_fields = ['user', ]
    exclude = ['status', ]
    actions = ['block_user_permissions', 'unlock_user_permissions', ]

    @admin.action(description='Bloquear usuários para criação de conteúdo')
    def block_user_permissions(self, request, queryset):
        for user_report_register in queryset:
            if user_report_register.status == 'b':
                continue

            user_report_register.status = 'b'
            user_report_register.save()

            user = user_report_register.user
            user.user_permissions.clear()

    @admin.action(description='Desbloquear usuários para criação de conteúdo')
    def unlock_user_permissions(self, request, queryset):
        for user_report_register in queryset:
            if user_report_register.status == 'n':
                continue

            user_report_register.status = 'n'
            user_report_register.reports = 0
            user_report_register.save()

            user = user_report_register.user
            model_permissions = [Post, Album, Image, Search, Option]
            for model in model_permissions:
                content_type = ContentType.objects.get_for_model(model)
                permissions = Permission.objects.filter(content_type=content_type)
                for permission in permissions:
                    user.user_permissions.add(permission)


admin.site.register(UserReportRegister, UserReportRegisterAdmin)
