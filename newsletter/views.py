from django.shortcuts import redirect, render, reverse
from django.contrib import messages
from django.utils import timezone as tz
from .models import NewsLetterUser


def newsletter_add_user(request):
    if not request.POST:
        return redirect(reverse('blog:index'))

    email = request.POST.get('email-newsletter')

    user = NewsLetterUser.objects.filter(email_newsletteruser=email)

    if user.count():
        if user[0].activated_newsletteruser:
            messages.success(request, 'E-mail já cadastrado')
            return redirect(reverse('blog:index'))
        else:
            user = user[0]
            user.activated_newsletteruser = True
            user.activated_date_newsletteruser = tz.now()
            user.save()
            return redirect(reverse('newsletter:done_add_user'))

    NewsLetterUser.objects.create(email_newsletteruser=email)
    return redirect(reverse('newsletter:done_add_user'))


def done_newsletter_add_user(request):
    return render(request, 'newsletter/done_newsletter.html')
