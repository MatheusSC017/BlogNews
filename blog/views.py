from django.shortcuts import render
from django.views.generic import TemplateView
from django.utils import timezone
from post import models as model_post
from album import models as model_album
from search import models as model_search


class Home(TemplateView):
    template_name = 'blog/home.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['posts'] = model_post.Post.objects.filter(
            published_post=True,
            published_date_post__lte=timezone.now()
        ).order_by('-published_date_post')[:2]
        context['galery'] = model_album.Image.objects.filter(
            album_image__published_album=True
        ).order_by('?')[:6]
        context['searches'] = model_search.Search.objects.filter(
            published_search=True,
        )

        return context


def about(request):
    return render(request, 'blog/about.html')
