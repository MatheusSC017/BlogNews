from django.shortcuts import reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.contrib import messages
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


class AlbumUpdate(LoginRequiredMixin, UpdateView):
    pass


class AlbumDelete(LoginRequiredMixin, DeleteView):
    pass
