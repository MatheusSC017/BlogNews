from django.contrib import admin
from django_summernote import admin as sn_admin
from django.core.mail import EmailMessage
from django.contrib import messages
from .models import NewsLetterUser, NewsLetterMessage


class NewsLetterUserAdmin(admin.ModelAdmin):
    list_display = ['email', 'creation_date',
                    'activated', 'activated_date', ]
    list_display_links = ['email', ]
    list_filter = ['activated', ]
    search_fields = ['email', ]


class NewsLetterMessageAdmin(sn_admin.SummernoteModelAdmin):
    list_display = ['title', 'creation_date',
                    'edition_date', 'published', ]
    list_display_links = ['title', ]
    list_filter = ['published', ]
    search_fields = ['title', ]
    summernote_fields = ['message', ]
    exclude = ['published', ]
    actions = ['send_newsletter', ]

    @admin.action(description='Enviar a mensagem para todos os usuários')
    def send_newsletter(self, request, queryset):
        email_user = NewsLetterUser.objects.filter(activated=True)

        # Creating email and message lists
        email_user_list = [email.email for email in email_user]
        for message in queryset:
            email_message = EmailMessage(message.title,
                                         message.message,
                                         bcc=email_user_list)
            email_message.content_subtype = 'html'
            email_message.send(fail_silently=True)

        messages.success(request, str(queryset.count()) + ' mensagem(ns) enviadas com sucesso.')
        queryset.update(published=True)


admin.site.register(NewsLetterUser, NewsLetterUserAdmin)
admin.site.register(NewsLetterMessage, NewsLetterMessageAdmin)
