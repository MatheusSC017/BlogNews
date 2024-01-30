from django.shortcuts import redirect, render, reverse
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView
from django.template import loader
from django.core.mail import EmailMessage
from django.utils.crypto import get_random_string
from django.contrib import messages
from django.utils import timezone as tz
from .models import NewsLetterUser


def newsletter_add_user(request):
    if not request.POST:
        return redirect(reverse('blog:index'))

    email = request.POST.get('email-newsletter')

    user = NewsLetterUser.objects.filter(email=email)

    if user.count():
        if user[0].activated:
            messages.success(request, 'E-mail já cadastrado')
            return redirect(reverse('blog:index'))
        else:
            user = user[0]
            user.activated = True
            user.activated_date = tz.now()
            user.save()
            return redirect(reverse('newsletter:done_add_user'))

    NewsLetterUser.objects.create(email=email)
    return redirect(reverse('newsletter:done_add_user'))


def done_newsletter_add_user(request):
    return render(request, 'newsletter/done_newsletter.html')


class UnsubscribeNewsletter(View):
    template_name = 'newsletter/unsubscribe_newsletter.html'
    email_template_name = 'newsletter/unsubscribe_newsletter_email.html'
    success_url = reverse_lazy('newsletter:unsubscribe_done')
    use_https = False

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email-newsletter')

        token = get_random_string(length=32)
        request.session[token] = email

        self.send_email(email, token)

        return redirect(self.get_success_url())

    def send_email(self, email, token):
        from_email = settings.EMAIL_HOST_USER
        to = email
        subject = 'Cancelamento da inscrição'
        body = loader.render_to_string(self.email_template_name, self.get_email_context(to, token))

        email_message = EmailMessage(subject, body, from_email, (to, ))
        email_message.send()

    def get_success_url(self):
        return self.success_url

    def get_email_context(self, email, token):
        current_site = get_current_site(self.request)
        domain = current_site.domain
        site_name = current_site.name
        context = {'email': email,
                   'domain': domain,
                   'site_name': site_name,
                   'token': token,
                   'protocol': 'https' if self.use_https else 'http'}
        return context


class DoneUnsubscribeNewsletter(TemplateView):
    template_name = 'newsletter/done_unsubscribe_newsletter.html'


class ConfirmUnsubscribeNewsletter(View):
    template_name = 'newsletter/confirm_unsubscribe_newsletter.html'
    success_url = reverse_lazy('newsletter:unsubscribe_finish')

    def get(self, request, *args, **kwargs):
        context = self.get_context()
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        context = self.get_context()

        if context['valid_token']:
            del request.session[kwargs.get('token')]
            user = NewsLetterUser.objects.filter(email=context['email'])

            # Check if the e-mail is registered in the database
            if user.count():
                user = user[0]
                # Check if the user is activated
                if user.activated:
                    user.activated = False
                    user.save()
                    return redirect(self.get_success_url())

            messages.error(request, 'E-mail não cadastrado')
            return redirect(reverse('blog:index'))
        else:
            return render(request, self.template_name, context)

    def get_context(self):
        context = {}

        email = self.request.session.get(self.kwargs.get('token'))
        context['email'] = email
        context['valid_token'] = email is not None

        return context

    def get_success_url(self):
        return self.success_url


class FinishUnsubscribeNewsletter(TemplateView):
    template_name = 'newsletter/finish_unsubscribe_newsletter.html'
