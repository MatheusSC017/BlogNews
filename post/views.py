from django.shortcuts import redirect, reverse, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.db.models import Q, Count, Avg
from django.contrib import messages
from django.utils import timezone
from .models import Post as PostModel, Category as CategoryModel, RattingUserPost
from comment.models import Comment
from comment.forms import CommentForm


class Blog(ListView):
    """
    Blog Page

    List of published posts with search tool by category, text and sorting

    """
    template_name = 'post/blog.html'
    model = PostModel
    paginate_by = 10
    context_object_name = 'posts'
    category = None
    order_by = '-published_date_post'
    search = None

    def get_queryset(self, *args, **kwargs):
        """
        Blog Search

        Searches for published posts, returning the number of comments, title, excerpt, image, rating and
        publication date

        :param args: Other Arguments without key
        :param kwargs: Other Arguments with key
        :return: QuerySet Object
        """
        qs = super().get_queryset(*args, **kwargs)

        qs = qs.annotate(
            comments_post=Count('comment', distinct=True),
            ratting_post=Avg('rattinguserpost__ratting', distinct=True)
        )

        if self.category is not None:
            qs = qs.filter(category_post=self.category)

        if self.search is not None:
            qs = qs.filter(Q(title_post__icontains=self.search) | Q(excerpt_post__icontains=self.search))

        qs = qs.filter(published_post=True).order_by(self.order_by)

        qs = qs.defer('description_post')

        return qs

    def get_context_data(self, *args, **kwargs):
        """ Include the list of posts and the request to the context """
        context = super().get_context_data(*args, **kwargs)

        context['categories'] = CategoryModel.objects.all()

        get_request = dict(self.request.GET)
        if get_request.get('category'):
            get_request['category'][0] = int(get_request['category'][0])
        context['get_request'] = get_request

        return context

    def get(self, request, *args, **kwargs):
        """ Receipt of data for research """
        category_field = request.GET.get('category')
        search_field = request.GET.get('search')
        order_by_field = request.GET.get('order_by')

        if category_field in [str(_.pk) for _ in CategoryModel.objects.all().defer('title_category')]:
            self.category = category_field

        if search_field != '':
            self.search = search_field

        order_list = {
            'publicacao': '-published_date_post',
            'avaliacao': '-ratting_post',
        }
        if order_by_field in order_list.keys():
            self.order_by = order_list[order_by_field]

        return super().get(request, *args, **kwargs)


class Post(DetailView):
    """
    PostPage

    Show Details about the post and registered comments
    """
    template_name = 'post/post.html'
    model = PostModel
    context_object_name = 'post'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        post = context['post']
        if not post.published_post:
            return redirect(reverse('post:blog'))

        response = self.render_to_response(context)

        if request.COOKIES.get('view-flag') != str(post.pk):
            if request.user.is_authenticated:
                post.user_views_post += 1
            else:
                post.anonymous_views_post += 1

            post.save()

            response.set_cookie('view-flag', post.pk)

        return response

    def get_queryset(self, *args, **kwargs):
        """ Returns the data of the Post """
        qs = super().get_queryset(*args, **kwargs)

        qs = qs.annotate(
            comments_post=Count('comment', distinct=True),
            ratting_post=Avg('rattinguserpost__ratting', distinct=True),
        )

        return qs

    def get_context_data(self, *args, **kwargs):
        """ Adds the registered comments and the comment form to the context"""
        context = super().get_context_data(*args, **kwargs)

        comments_qs = Comment.objects.select_related('user_comment').filter(post_comment=context.get('post').pk)

        context['comments'] = comments_qs
        context['comment_form'] = CommentForm(self.request.POST or None)
        if self.request.user.is_authenticated:
            ratting_user = RattingUserPost.objects.filter(user_ratting=self.request.user,
                                                          post_ratting=context['post'])
            if ratting_user.count() == 1:
                context['ratting_user'] = ratting_user[0].ratting

        return context

    def post(self, request, *args, **kwargs):
        """ Registration of the comment """
        if not request.user.is_authenticated:
            return redirect(reverse('user:login'))

        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        if not context['post'].published_post:
            return redirect(reverse('post:blog'))

        action = {'create-comment': self.create_comment,
                  'update-comment': self.update_comment,
                  'delete-comment': self.delete_comment,
                  'ratting-post': self.ratting_post, }

        response = None
        try:
            response = action[request.POST.get('action')](request, context)
        except KeyError:
            messages.error(request, 'Ação inválida')

        if response is None:
            response = redirect(reverse('post:post', kwargs={'pk': kwargs.get('pk')}))

        return response

    def create_comment(self, request, context):
        form = context.get('comment_form')

        if not form.is_valid():
            return self.render_to_response(context)

        comment = form.save(commit=False)

        comment.user_comment = request.user
        comment.post_comment = context.get('post')
        comment.save()
        messages.success(request, 'Comentário adicionado')

    def update_comment(self, request, context):
        form = context.get('comment_form')

        if not form.is_valid():
            return self.render_to_response(context)

        try:
            comment = get_object_or_404(Comment, pk=request.POST.get('comment-pk'))

            if comment.post_comment != context.get('post'):
                messages.error(request, 'Comentário inválido')
                return self.render_to_response(context)
        except ValueError:
            messages.error(request, 'Comentário não encontrado')
            return self.render_to_response(context)

        if comment.user_comment != request.user:
            messages.error(request, 'Usuário inválido')
            return self.render_to_response(context)

        comment.comment = request.POST.get('comment')
        comment.edition_date_comment = timezone.now()

        comment.save()
        messages.success(request, 'Comentário editado')

    def delete_comment(self, request, context):
        try:
            comment = get_object_or_404(Comment, pk=request.POST.get('comment-pk'))

            if comment.post_comment != context.get('post'):
                messages.error(request, 'Comentário inválido')
                return self.render_to_response(context)
        except ValueError:
            messages.error(request, 'Comentário não encontrado')
            return self.render_to_response(context)

        if comment.user_comment != request.user:
            messages.error(request, 'Usuário inválido')
            return self.render_to_response(context)

        comment.delete()
        messages.success(request, 'Comentário deletado')

    def ratting_post(self, request, context):
        try:
            ratting = int(self.request.POST.get('star'))

            if 1 > ratting or ratting > 5:
                messages.error(request, 'Avaliação inválida')
                return self.render_to_response(context)
        except TypeError:
            messages.error(request, 'Falha na avaliação')
            return self.render_to_response(context)

        ratting_post = RattingUserPost.objects.filter(user_ratting=request.user,
                                                      post_ratting=context.get('post'))

        if ratting_post.count() == 0:
            RattingUserPost.objects.create(user_ratting=request.user,
                                           post_ratting=context.get('post'),
                                           ratting=ratting)
        else:
            ratting_post = ratting_post[0]
            ratting_post.ratting = ratting
            ratting_post.save()

        messages.success(request, 'Obrigado pelo Feedback')
