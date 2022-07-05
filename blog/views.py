from django.shortcuts import render
from django.views.generic import TemplateView
from django.db.models import Max, Count, Subquery, OuterRef
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
        ).defer('description_post').order_by('-published_date_post')[:2]

        context['galery'] = model_album.Image.objects.filter(
            album_image__published_album=True
        ).order_by('?')[:6]

        options = model_search.Option.objects.filter(
            search_option=OuterRef('pk')
        ).annotate(
            vote_option=Count('vottinguseroption')
        ).order_by('-vote_option')[:1]
        context['searches'] = model_search.Search.objects.filter(
            published_search=True,
            publication_date_search__lte=timezone.now()
        ).annotate(
            max_option=Subquery(options.values('response_option'))
        ).order_by('-publication_date_search')[:3]

        return context


def about(request):
    return render(request, 'blog/about.html')
