from django.shortcuts import redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.utils import timezone as tz
from .forms import CommentForm
from .models import Comment
from post.models import Post
from utils.utils import verify_recaptcha


@login_required(login_url=settings.LOGIN_URL)
def create_comment(request, post_pk):
    """ Registration of the comment """
    if not request.POST:
        return redirect(reverse('post:post', args=[post_pk, ]))

    post = get_object_or_404(Post, pk=post_pk, published=True, publication_date__lte=tz.now())
    form = CommentForm(request.POST)
    recaptcha_response = request.POST.get('g-recaptcha-response')

    if not verify_recaptcha(recaptcha_response):
        messages.warning(request, 'ReCaptcha inválido')
        return redirect(reverse('post:post', args=[post_pk, ]))

    if not form.is_valid():
        return redirect(reverse('post:post', args=[post_pk, ]))

    comment = form.save(commit=False)

    comment.user = request.user
    comment.post = post
    comment.save()
    messages.success(request, 'Comentário adicionado')
    return redirect(reverse('post:post', args=[post_pk, ]))


@login_required(login_url=settings.LOGIN_URL)
def update_comment(request, post_pk):
    """ Update the comment """
    if not request.POST:
        return redirect(reverse('post:post', args=[post_pk, ]))

    post = get_object_or_404(Post, pk=post_pk, published=True, publication_date__lte=tz.now())
    comment = get_object_or_404(Comment,
                                pk=request.POST['primary-key'],
                                post=post,
                                user=request.user)
    form = CommentForm(request.POST, instance=comment)

    if not form.is_valid():
        return redirect(reverse('post:post', args=[post_pk, ]))

    form .save(commit=False)
    form.edition_date_comment = tz.now()
    form.save()

    messages.success(request, 'Comentário editado')
    return redirect(reverse('post:post', args=[post_pk, ]))


@login_required(login_url=settings.LOGIN_URL)
def delete_comment(request, post_pk):
    """ Delete the comment """
    if not request.POST:
        return redirect(reverse('post:post', args=[post_pk, ]))

    post = get_object_or_404(Post, pk=post_pk, published=True, publication_date__lte=tz.now())
    comment = get_object_or_404(Comment,
                                pk=request.POST['primary-key'],
                                post=post.pk,
                                user=request.user.pk)

    comment.delete()
    messages.success(request, 'Comentário deletado')
    return redirect(reverse('post:post', args=[post_pk, ]))
