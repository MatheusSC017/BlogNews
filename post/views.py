from django.conf import settings
from django.shortcuts import redirect, reverse, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Q, Count, Avg
from django.contrib import messages
from django.utils import timezone as tz
from .models import Post as PostModel, Category as CategoryModel, RattingUserPost
from album import models as album_models
from comment.models import Comment
from comment.forms import CommentForm
from .forms import PostForm


class BlogTemplate(ListView):
    """ List of posts with search tool by category, text and sorting """
    model = PostModel
    paginate_by = 10
    context_object_name = 'posts'
    category = None
    order_by = '-publication_date_post'
    search = None

    def get_queryset(self, *args, **kwargs):
        """
        Blog Search

        Searches for posts, returning the number of comments, title, excerpt, image, rating and
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

        qs = qs.order_by(self.order_by)

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
            'publicacao': '-publication_date_post',
            'avaliacao': '-ratting_post',
        }
        if order_by_field in order_list.keys():
            self.order_by = order_list[order_by_field]

        return super().get(request, *args, **kwargs)


class Blog(BlogTemplate):
    """ List only the published posts """
    template_name = 'post/blog.html'

    def get_queryset(self, *args, **kwargs):
        """ Select only the published posts """
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(publication_date_post__lte=tz.now())
        qs = qs.filter(published_post=True)
        return qs


class Post(DetailView):
    """  Show Details about the post and registered comments """
    template_name = 'post/post.html'
    model = PostModel
    context_object_name = 'post'

    def get(self, request, *args, **kwargs):
        """ Check if the post is published and the post view system """
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        post = context['post']
        if not post.published_post:
            return redirect(reverse('post:blog'))

        response = self.render_to_response(context)

        """" Check the flag to avoid repeated views """
        if request.COOKIES.get('view-flag') != str(post.pk):
            """ Separetes views of anonymous users and logged in users """
            if request.user.is_authenticated:
                post.user_views_post += 1
            else:
                post.anonymous_views_post += 1

            post.save()

            response.set_cookie('view-flag', post.pk)

        return response

    def post(self, request, *args, **kwargs):
        """ Registration/ update the ratting of user """
        if not request.user.is_authenticated:
            return redirect(reverse('user:login'))

        post = get_object_or_404(PostModel, pk=kwargs.get('pk'), published_post=True, publication_date_post__lte=tz.now())

        try:
            ratting = int(request.POST.get('star'))
        except TypeError:
            messages.error(request, 'Falha na avaliação')
            return redirect(reverse('post:post', kwargs={'pk': kwargs.get('pk')}))

        if 1 > ratting or ratting > 5:
            messages.error(request, 'Avaliação inválida')
            return redirect(reverse('post:post', kwargs={'pk': kwargs.get('pk')}))

        ratting_post = RattingUserPost.objects.filter(user_ratting=request.user,
                                                      post_ratting=post)

        if ratting_post.count() == 0:
            RattingUserPost.objects.create(user_ratting=request.user,
                                           post_ratting=post,
                                           ratting=ratting)
        else:
            ratting_post = ratting_post[0]
            ratting_post.ratting = ratting
            ratting_post.save()

        messages.success(request, 'Obrigado pelo Feedback')
        return redirect(reverse('post:post', kwargs={'pk': kwargs.get('pk')}))

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


class BlogUser(LoginRequiredMixin, PermissionRequiredMixin, BlogTemplate):
    """ List the user posts """
    template_name = 'post/blog_user.html'
    login_url = settings.LOGIN_URL
    permission_required = 'post.view_post'
    permission_denied_message = 'Necessário usuário autorizado'

    def get_queryset(self, *args, **kwargs):
        """ Select only the user posts """
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(user_post=self.request.user)
        return qs

    def post(self, *args, **kwargs):
        """ Publish or unpublish the post """
        try:
            post = get_object_or_404(PostModel,
                                     pk=self.request.POST['primary-key'],
                                     user_post=self.request.user.pk)
            post.published_post = not post.published_post
            if post.published_post:
                messages.success(self.request, 'Post publicado')
            else:
                messages.error(self.request, 'Post despublicado')
            post.save()
        except (KeyError, ValueError):
            messages.error(self.request, 'Post não encontrado')

        return redirect(reverse('post:user_blog'))


class RegisterPost(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """ Page to register the Post """
    template_name = 'post/post_user.html'
    model = PostModel
    form_class = PostForm
    login_url = settings.LOGIN_URL
    permission_required = 'post.add_post'
    permission_denied_message = 'Necessário usuário autorizado'

    def get_form(self, form_class=None):
        """ Select only the user albuns """
        form = super().get_form(form_class)

        form.fields['album_post'].queryset = album_models.Album.objects.filter(
            user_album=self.request.user.pk
        )

        return form

    def post(self, request, *args, **kwargs):
        """ Includes the user and check the form """
        form = self.get_form()
        if form.is_valid():
            form = form.save(commit=False)
            form.user_post = request.user
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self, *args, **kwargs):
        """ redirects to posts page if registration was successful """
        messages.success(self.request, 'Post adicionado')
        return reverse('post:user_blog')


class UpdatePost(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """ Update the post """
    template_name = 'post/post_user.html'
    model = PostModel
    form_class = PostForm
    login_url = settings.LOGIN_URL
    permission_required = 'post.change_post'
    permission_denied_message = 'Necessário usuário autorizado'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        if self.object.user_post != request.user:
            return redirect(reverse('post:user_blog'))

        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        if self.object.user_post != request.user:
            return redirect(reverse('post:user_blog'))

        return super().post(request, *args, **kwargs)

    def get_form(self, form_class=None):
        """ Select only the user albuns """
        form = super().get_form(form_class)

        form.fields['album_post'].queryset = album_models.Album.objects.filter(
            user_album=self.request.user.pk
        )

        return form

    def get_success_url(self, *args, **kwargs):
        """ Redirect the user to posts page """
        messages.success(self.request, 'Post atualizado')
        return reverse('post:user_blog')
