from django.shortcuts import reverse, redirect, get_object_or_404
from django.views.generic import View, ListView, CreateView, DetailView
from django.views.generic.edit import FormMixin
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.http import JsonResponse
from django.db.models import Count
from django.contrib import messages
from django.conf import settings
from . import forms
from . import models
from report.models import Report


class Album(ListView):
    """ Page with all published albuns with 3 images or more """
    template_name = 'album/album.html'
    model = models.Album
    paginate_by = None
    context_object_name = 'albuns'
    continuos_load = 6

    def get_queryset(self, *args, **kwargs):
        """ Select the published albuns and check if the album has 3 images or more"""
        qs = super().get_queryset(*args, **kwargs)

        qs = qs.filter(published=True)
        qs = qs.annotate(
            count_images=Count('image__album')
        ).filter(count_images__gte=3)[:self.continuos_load]

        return qs

    def get_context_data(self, *args, **kwargs):
        """ Add the images for each album """
        context = super().get_context_data(*args, **kwargs)

        albuns_images = list()
        for album in context['albuns']:
            albuns_images.append({'album': album,
                                  'images': models.Image.objects.filter(album=album.pk)[:3], })
        context['albuns'] = albuns_images
        context['number_of_albums'] = len(albuns_images)

        return context


def load_more_albuns(request):
    continuos_load = 6

    offset = request.GET.get('offset')

    qs = models.Album.objects.all()
    qs = qs.filter(published=True)
    qs = qs.annotate(
        count_images=Count('image__album')
    ).filter(count_images__gte=3)[int(offset): int(offset) + continuos_load]

    albuns_images = list()
    for album in qs:
        albuns_images.append({'album': album,
                              'images': models.Image.objects.filter(album=album.pk)[:3], })

    data = [
        {
            'pk': album['album'].pk,
            'title': album['album'].title,
            'main_image': album['images'][0].image.url,
            'second_image': album['images'][0].image.url,
            'third_image': album['images'][0].image.url
        } for album in albuns_images
    ]
    return JsonResponse(data, safe=False)


class AlbumImages(DetailView):
    """ Shows all images of the selected album """
    template_name = 'album/images.html'
    model = models.Album
    context_object_name = 'album'

    def get_context_data(self, *args, **kwargs):
        """ Select the images of the album """
        context = super().get_context_data(*args, **kwargs)
        context['images'] = models.Image.objects.filter(album=context.get('album').pk)
        return context

    def get(self, request, *args, **kwargs):
        """ Make sure the album has been published and the number of images is 3 or more """
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)

        if not context['album'].published:
            return redirect(reverse('album:album'))

        if context['images'].count() < 3:
            return redirect(reverse('album:album'))

        return self.render_to_response(context)


class AlbumUser(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """ Shows all the user albuns """
    template_name = 'album/album_user.html'
    model = models.Album
    paginate_by = 10
    context_object_name = 'albuns'
    login_url = settings.LOGIN_URL
    permission_required = 'album.view_album'
    permission_denied_message = 'Necessário usuário autorizado'

    def get_queryset(self, *args, **kwargs):
        """ Select only the user albuns """
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(user=self.request.user.pk)
        return qs

    def get_context_data(self, *args, **kwargs):
        """ Add the album form to the context """
        context = super().get_context_data(*args, **kwargs)
        context['album_form'] = forms.AlbumForm(self.request.POST or None)
        return context


class AlbumCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """ Page to create a new album """
    template_name = 'album/album_create.html'
    model = models.Album
    form_class = forms.AlbumForm
    login_url = settings.LOGIN_URL
    permission_required = 'album.add_album'
    permission_denied_message = 'Necessário usuário autorizado'

    def post(self, request, *args, **kwargs):
        """ Make sure the form is valid e add the required fields """
        form = self.get_form()
        if form.is_valid():
            form = form.save(commit=False)
            form.user = request.user
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        """ Success message """
        messages.success(self.request, 'Álbum cadastrado')
        return reverse('album:user_album')


@login_required(login_url=settings.LOGIN_URL)
@permission_required(perm='album.change_album')
def album_update(request):
    """ Method to update the selected album """
    if request.POST:
        pk = request.POST.get('primary-key')
        if pk is not None:
            album = get_object_or_404(models.Album, pk=pk, user=request.user)
            form = forms.AlbumForm(request.POST, instance=album)
            if form.is_valid():
                form.save()
                messages.success(request, 'Álbum editado')
                return redirect(reverse('album:user_album'))
            else:
                messages.error(request, 'Dados incorretos')
                return redirect(reverse('album:user_album'))
        else:
            messages.error(request, 'Álbum não encontrado')
            return redirect(reverse('album:user_album'))
    else:
        return redirect(reverse('album:user_album'))


@login_required(login_url=settings.LOGIN_URL)
@permission_required(perm='album.delete_album')
def album_delete(request):
    """ Method to delete the selected album """
    if request.POST:
        pk = request.POST.get('primary-key')
        if pk is not None:
            album = get_object_or_404(models.Album, pk=pk, user=request.user)
            album.delete()
            messages.error(request, 'Álbum deletado')
            return redirect(reverse('album:user_album'))
        else:
            messages.error(request, 'Álbum não encontrado')
            return redirect(reverse('album:user_album'))
    else:
        return redirect(reverse('album:user_album'))


class AlbumImagesUser(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    """ Page with all the images of user album """
    template_name = 'album/album_images.html'
    model = models.Album
    context_object_name = 'album'
    login_url = settings.LOGIN_URL
    permission_required = 'album.view_image'
    permission_denied_message = 'Necessário usuário autorizado'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        if context['album'].user != request.user:
            return redirect(reverse('album:user_album'))
        return self.render_to_response(context)

    def get_context_data(self, *args, **kwargs):
        """ Add all the images to the context and the form to add new images """
        context = super().get_context_data(*args, **kwargs)

        context['images'] = models.Image.objects.filter(album=context.get('album').pk)
        context['image_form'] = forms.ImageForm()

        return context


class UploadImages(LoginRequiredMixin, PermissionRequiredMixin, View, FormMixin):
    """ Page to view the images of the user album and upload new images """
    form_class = forms.ImageForm
    login_url = settings.LOGIN_URL
    permission_required = 'album.add_image'
    permission_denied_message = 'Necessário usuário autorizado'

    def post(self, request, *args, **kwargs):
        """ Upload the selected images """
        form = self.get_form()
        album = get_object_or_404(models.Album, pk=kwargs.get('pk'), user=request.user.pk)
        if form.is_valid():
            files = request.FILES.getlist('image_field')
            for f in files:
                models.Image.objects.create(album=album,
                                            image=f)
            messages.success(self.request, 'Imagens cadastradas')
            return redirect(reverse('album:user_images', args=[album.pk, ]))
        else:
            messages.error(self.request, 'Erro no cadastramento')
            return redirect(reverse('album:user_images', args=[album.pk, ]))


@login_required(login_url=settings.LOGIN_URL)
@permission_required(perm='album.change_image')
def image_update_title(request, pk):
    """ Update the image title """
    album = get_object_or_404(models.Album, pk=pk, user=request.user.pk)
    if request.POST:
        image_pk = request.POST.get('primary-key')
        title = request.POST.get('title')
        if len(title) < 5:
            messages.error(request, 'Título deve possuir ao menos 5 caracteres')
            return redirect(reverse('album:user_images', args=[album.pk, ]))

        image = get_object_or_404(models.Image, pk=image_pk, album=album.pk)
        image.title = title
        image.save()
        messages.success(request, 'Título editado')
        return redirect(reverse('album:user_images', args=[album.pk, ]))
    else:
        return redirect(reverse('album:user_images', args=[album.pk, ]))


@login_required(login_url=settings.LOGIN_URL)
@permission_required(perm='album.delete_image')
def image_delete(request, pk):
    """ Delete the selected image """
    album = get_object_or_404(models.Album, pk=pk, user=request.user)
    if request.POST:
        image_pk = request.POST.get('primary-key')
        image = get_object_or_404(models.Image, pk=image_pk, album=album.pk)
        image.delete()
        messages.success(request, 'Imagem deletada')
        return redirect(reverse('album:user_images', args=[album.pk, ]))
    else:
        return redirect(reverse('album:user_images', args=[album.pk, ]))


@login_required(login_url=settings.LOGIN_URL)
@permission_required(perm='album.delete_image')
def multiple_image_delete(request, pk):
    """ Method to delete multiple images at the same time """
    if request.POST:
        images_pk = request.POST.getlist('delete-items') or []
        if len(images_pk):
            album = get_object_or_404(models.Album, pk=pk, user=request.user.pk)
            images = models.Image.objects.filter(pk__in=images_pk, album=album.pk)
            images.delete()
            messages.success(request, "Imagens excluidas")
        return redirect(reverse('album:user_images', args=[pk, ]))
    else:
        return redirect(reverse('album:user_images', args=[pk, ]))


def register_report(request):
    if not request.POST:
        return redirect(reverse('album:album'))

    pk = request.POST.get('primary-key')

    if not pk:
        messages.error(request, 'Album não encontrado')
        return redirect(reverse('album:album'))

    album = get_object_or_404(models.Album, pk=pk, published_album=True)
    report_description = request.POST.get('report-description')

    if not report_description.strip():
        messages.error(request, 'A denúncia não pode estar vázia')
        return redirect(reverse('album:image', kwargs={'pk': pk, }))

    description = 'Album: {}, Autor: {} - {}'.format(pk, album.user, report_description)

    Report.objects.create(user=album.user, description=description)
    messages.success(request, 'Sua denúncia foi registrada')
    return redirect(reverse('album:image', kwargs={'pk': pk, }))
