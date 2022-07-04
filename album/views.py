from django.shortcuts import reverse, redirect, get_object_or_404
from django.views.generic import View, ListView, CreateView, DetailView
from django.views.generic.edit import FormMixin
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Count
from django.contrib import messages
from django.conf import settings
from . import forms
from . import models


class Album(ListView):
    template_name = 'album/album.html'
    model = models.Album
    paginate_by = 6
    context_object_name = 'albuns'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)

        qs = qs.filter(published_album=True)
        qs = qs.annotate(
            count_images=Count('image__album_image')
        ).filter(count_images__gte=3)

        return qs

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        albuns_images = list()
        for album in context['albuns']:
            albuns_images.append({'album': album,
                                  'images': models.Image.objects.filter(album_image=album.pk)[:3], })
        context['albuns'] = albuns_images

        return context


class AlbumImages(DetailView):
    template_name = 'album/images.html'
    model = models.Album
    context_object_name = 'album'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['images'] = models.Image.objects.filter(album_image=context.get('album').pk)
        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)

        if not context['album'].published_album:
            return redirect(reverse('album:album'))

        if context['images'].count() < 3:
            return redirect(reverse('album:album'))

        return self.render_to_response(context)


class AlbumUser(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    template_name = 'album/album_user.html'
    model = models.Album
    paginate_by = 10
    context_object_name = 'albuns'
    login_url = settings.LOGIN_URL
    permission_required = 'album.view_album'
    permission_denied_message = 'Necessário usuário autorizado'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(user_album=self.request.user.pk)
        return qs

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['album_form'] = forms.AlbumForm(self.request.POST or None)
        return context


class AlbumCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    template_name = 'album/album_create.html'
    model = models.Album
    form_class = forms.AlbumForm
    login_url = settings.LOGIN_URL
    permission_required = 'album.add_album'
    permission_denied_message = 'Necessário usuário autorizado'

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            form = form.save(commit=False)
            form.user_album = request.user
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        messages.success(self.request, 'Álbum cadastrado')
        return reverse('album:user_album')


@login_required(login_url=settings.LOGIN_URL)
@permission_required(perm='album.change_album')
def album_update(request):
    pk = request.POST.get('primary-key')
    form = forms.AlbumForm(request.POST)
    if pk is not None:
        album = get_object_or_404(models.Album, pk=pk, user_album=request.user)
        if form.is_valid():
            album_form = form.save(commit=False)
            album_form.pk = album.pk
            album_form.user_album = album.user_album
            album_form.save()
            messages.success(request, 'Álbum editado')
            return redirect(reverse('album:user_album'))
        else:
            messages.error(request, 'Dados incorretos')
            return redirect(reverse('album:user_album'))
    else:
        messages.error(request, 'Álbum não encontrado')
        return redirect(reverse('album:user_album'))


@login_required(login_url=settings.LOGIN_URL)
@permission_required(perm='album.delete_album')
def album_delete(request):
    pk = request.POST.get('primary-key')
    if pk is not None:
        album = get_object_or_404(models.Album, pk=pk, user_album=request.user)
        album.delete()
        messages.error(request, 'Álbum deletado')
        return redirect(reverse('album:user_album'))
    else:
        messages.error(request, 'Álbum não encontrado')
        return redirect(reverse('album:user_album'))


class AlbumImagesUser(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    template_name = 'album/album_images.html'
    model = models.Album
    context_object_name = 'album'
    login_url = settings.LOGIN_URL
    permission_required = 'album.view_image'
    permission_denied_message = 'Necessário usuário autorizado'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['images'] = models.Image.objects.filter(album_image=context.get('album').pk)
        context['image_form'] = forms.ImageForm()

        return context


class UploadImages(LoginRequiredMixin, PermissionRequiredMixin, View, FormMixin):
    form_class = forms.ImageForm
    login_url = settings.LOGIN_URL
    permission_required = 'album.add_image'
    permission_denied_message = 'Necessário usuário autorizado'

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        album = get_object_or_404(models.Album, pk=kwargs.get('pk'), user_album=request.user.pk)
        if form.is_valid():
            files = request.FILES.getlist('image_field')
            for f in files:
                models.Image.objects.create(album_image=album,
                                            image=f)
            messages.success(self.request, 'Imagens cadastradas')
            return redirect(reverse('album:user_images', args=[album.pk, ]))
        else:
            messages.error(self.request, 'Erro no cadastramento')
            return redirect(reverse('album:user_images', args=[album.pk, ]))


@login_required(login_url=settings.LOGIN_URL)
@permission_required(perm='album.change_image')
def image_update_title(request, pk):
    album = get_object_or_404(models.Album, pk=pk, user_album=request.user.pk)
    image_pk = request.POST.get('primary-key')
    title = request.POST.get('title_image')
    if len(title) < 5:
        messages.error(request, 'Título deve possuir ao menos 5 caracteres')
        return redirect(reverse('album:user_images', args=[album.pk, ]))

    image = get_object_or_404(models.Image, pk=image_pk, album_image=album.pk)
    image.title_image = title
    image.save()
    messages.success(request, 'Título editado')
    return redirect(reverse('album:user_images', args=[album.pk, ]))


@login_required(login_url=settings.LOGIN_URL)
@permission_required(perm='album.delete_image')
def image_delete(request, pk):
    album = get_object_or_404(models.Album, pk=pk, user_album=request.user)
    image_pk = request.POST.get('primary-key')
    image = get_object_or_404(models.Image, pk=image_pk, album_image=album.pk)
    image.delete()
    messages.success(request, 'Imagem deletada')
    return redirect(reverse('album:user_images', args=[album.pk, ]))


@login_required(login_url=settings.LOGIN_URL)
@permission_required(perm='album.delete_image')
def multiple_image_delete(request, pk):
    images_pk = request.POST.getlist('delete-items') or []
    if len(images_pk):
        album = get_object_or_404(models.Album, pk=pk, user_album=request.user.pk)
        images = models.Image.objects.filter(pk__in=images_pk, album_image=album.pk)
        images.delete()
        messages.success(request, "Imagens excluidas")
    return redirect(reverse('album:user_images', args=[pk, ]))
