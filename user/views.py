from django.views.generic.base import View, TemplateResponseMixin
from django.views.generic.edit import CreateView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Permission, ContentType
from django.contrib.auth.views import FormView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, reverse
from django.contrib import messages
from django.conf import settings
from .forms import UserCreationFormBlog, UserChangeFormBlog
from post.models import Post
from album.models import Album, Image
from search.models import Search, Option


class Login(View, TemplateResponseMixin):
    """ Page to user login in the system """
    template_name = 'user/login.html'

    def get(self, *args, **kwargs):
        """ Check if the user is already logged in """
        if self.request.user.is_authenticated:
            messages.warning(self.request, 'Usuário já logado')
            return redirect(reverse('blog:index'))

        return self.render_to_response({})

    def post(self, *args, **kwargs):
        """ Check the user data and login """
        username = self.request.POST.get('username')
        password = self.request.POST.get('password')

        if self.request.user.is_authenticated:
            messages.warning(self.request, 'Usuário já logado')
            return redirect(reverse('blog:index'))

        user = authenticate(self.request, username=username, password=password)
        if user is not None:
            login(self.request, user=user)
            messages.success(self.request, 'Usuário logado')
            return redirect(reverse('blog:index'))
        else:
            messages.error(self.request, 'Usuário ou senha incorretos')
            return self.render_to_response({})


@login_required(login_url=settings.LOGIN_URL)
def logout_user(request):
    """ Check if the user is already logged out, if not, the user is logged out """
    logout(request)
    messages.success(request, 'Usuário deslogado')
    return redirect(reverse('blog:index'))


class Register(CreateView):
    """ Register user page """
    template_name = 'user/register.html'
    model = User
    form_class = UserCreationFormBlog

    def get(self, request, *args, **kwargs):
        """ Check if user is logged in """
        if request.user.is_authenticated:
            return redirect(reverse('blog:index'))

        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        """ Add the permissions of the user and redirect to login page """
        if self.request.POST.get('checkpermissions'):
            models_permissions = [Post, Album, Image, Search, Option, ]
            for model in models_permissions:
                content_type = ContentType.objects.get_for_model(model)
                post_permissions = Permission.objects.filter(content_type=content_type)
                for permission in post_permissions:
                    self.object.user_permissions.add(permission)
        messages.success(self.request, 'Usuário cadastrado')
        return reverse('user:login')


class Update(LoginRequiredMixin, FormView):
    template_name = 'user/update.html'
    model = User
    form_class = UserChangeFormBlog

    def get(self, request, *args, **kwargs):
        user_data = {
            'username': request.user.username,
            'email': request.user.email,
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
        }
        self.initial = user_data
        return super().get(request, *args, **kwargs)

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        return form_class(**self.get_form_kwargs(), instance=self.request.user)

    def form_valid(self, form):
        form.instance = self.request.user
        form.save()
        messages.success(self.request, "Perfil editado")
        return redirect(reverse('user:update'))
