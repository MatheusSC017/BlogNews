from django.contrib import admin
from django_summernote import admin as sn_admin
from django.core.mail import EmailMessage
from django.contrib import messages
from .models import NewsLetterUser, NewsLetterMessage


class NewsLetterUserAdmin(admin.ModelAdmin):
    list_display = ['email_newsletteruser', 'creation_date_newsletteruser',
                    'activated_newsletteruser', 'activated_date_newsletteruser', ]
    list_display_links = ['email_newsletteruser', ]
    list_filter = ['activated_newsletteruser', ]
    search_fields = ['email_newsletteruser', ]


class NewsLetterMessageAdmin(sn_admin.SummernoteModelAdmin):
    list_display = ['title_newslettermessage', 'creation_date_newslettermessage',
                    'edition_date_newslettermessage', 'published_newslettermessage', ]
    list_display_links = ['title_newslettermessage', ]
    list_filter = ['published_newslettermessage', ]
    search_fields = ['title_newslettermessage', ]
    summernote_fields = ['message_newslettermessage', ]
    exclude = ['published_newslettermessage', ]
    actions = ['send_newsletter', ]

    @admin.action(description='Enviar a mensagem para todos os usuários')
    def send_newsletter(self, request, queryset):
        email_user = NewsLetterUser.objects.filter(activated_newsletteruser=True)

        # Creating email and message lists
        email_user_list = [email.email_newsletteruser for email in email_user]
        for message in queryset:
            email_message = EmailMessage(message.title_newslettermessage,
                                         message.message_newslettermessage,
                                         bcc=email_user_list)
            email_message.content_subtype = 'html'
            email_message.send(fail_silently=True)

        messages.success(request, str(queryset.count()) + ' mensagem(ns) enviadas com sucesso.')
        queryset.update(published_newslettermessage=True)


admin.site.register(NewsLetterUser, NewsLetterUserAdmin)
admin.site.register(NewsLetterMessage, NewsLetterMessageAdmin)
