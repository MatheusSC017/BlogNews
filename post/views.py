from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.db.models import Count, Q
from .models import Post, Category
from comment.models import Comment


class Blog(ListView):
    template_name = 'post/blog.html'
    model = Post
    paginate_by = 10
    context_object_name = 'posts'
    category = None
    order_by = 'published_date_post'
    search = None

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

        qs = qs.filter(published_post=True).order_by(self.order_by)

        if self.category:
            qs = qs.filter(category_post=self.category)

        if self.search:
            qs = qs.filter(Q(title_post__icontains=self.search) | Q(excerpt_post__icontains=self.search))

        qs = qs.annotate(
            number_comments=Count(
                'comment',
                filter=Q(comment__published_comment=True)
            )
        )

        qs = qs.defer('description_post')

        return qs


    def get(self, request, *args, **kwargs):
        category_field = request.GET.get('category')
        search_field = request.GET.get('search')
        order_by_field = request.GET.get('order_by')

        if category_field in Category.objects.all():
            self.category = category_field

        if search_field != '':
            self.search = search_field

        if order_by_field in ['publication_date_post', 'ratting_post',]:
            self.order_by = order_by_field

        return super().get(request, *args, **kwargs)


class Post(DetailView):
    template_name = 'post/post.html'
    model = Post
    context_object_name = 'post'
