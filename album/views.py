from django.shortcuts import reverse, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.contrib import messages
from django.core.exceptions import PermissionDenied
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


class AlbumUser(LoginRequiredMixin, ListView):
    template_name = 'album/album_user.html'
    model = models.Album
    paginate_by = 10
    context_object_name = 'albuns'
    permission_denied_message = 'Necessário usuário autorizado'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm('album.view_album'):
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(user_album=self.request.user.pk)
        return qs

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['album_form'] = forms.AlbumForm(self.request.POST or None)
        return context


class AlbumCreate(LoginRequiredMixin, CreateView):
    template_name = 'album/album_create.html'
    model = models.Album
    form_class = forms.AlbumForm
    permission_denied_message = 'Necessário usuário autorizado'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm('album.add_album'):
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

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


@login_required
def album_update(request):
    if not request.user.has_perm('album.change_album'):
        raise PermissionDenied('Necessário usuário autorizado')

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

class AlbumDelete(LoginRequiredMixin, DeleteView):
    pass
