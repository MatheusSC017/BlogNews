from django.shortcuts import render
from django.views.generic import TemplateView
from django.db.models import Count, Subquery, OuterRef
from django.utils import timezone
from post import models as model_post
from album import models as model_album
from search import models as model_search


class Home(TemplateView):
    template_name = 'blog/home.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['posts'] = model_post.Post.objects.filter(
            published=True,
            publication_date__lte=timezone.now()
        ).defer('description').order_by('-publication_date')[:2]

        context['galery'] = model_album.Image.objects.filter(
            album__published=True
        ).order_by('?')[:6]

        options = model_search.Option.objects.filter(
            search=OuterRef('pk')
        ).annotate(
            vote=Count('vottinguseroption')
        ).order_by('-vote')[:1]
        context['searches'] = model_search.Search.objects.filter(
            published=True,
            publication_date__lte=timezone.now()
        ).annotate(
            max_option=Subquery(options.values('response'))
        ).order_by('-publication_date')[:3]

        return context


def about(request):
    return render(request, 'blog/about.html')
