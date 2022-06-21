from django.views.generic import ListView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
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

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(user_album=self.request.user.pk)
        return qs


class AlbumCreate(LoginRequiredMixin, CreateView):
    pass


class AlbumUpdate(LoginRequiredMixin, UpdateView):
    pass
