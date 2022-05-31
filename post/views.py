from django.shortcuts import render
from django.views.generic.list import ListView
from django.db.models import Count, Q
from .models import Post, Category
from comment.models import Comment


class Blog(ListView):
    template_name = 'post/blog.html'
    model = Post
    paginate_by = 10
    context_object_name = 'posts'

    def get_queryset(self, *args, **kwargs):
        '''
        Blog Search

        Searches for published posts, returning the number of comments, title, excerpt, image, rating and
        publication date

        :param args: Other Arguments without key
        :param kwargs: Other Arguments with key
        :return: QuerySet Object
        '''
        qs = super().get_queryset(*args, **kwargs)

        qs = qs.filter(published_post=True).order_by('publication_date_post')
        qs = qs.annotate(
            number_comments=Count(
                'comment',
                filter=Q(published_comment=True)
            )
        )

        return qs
