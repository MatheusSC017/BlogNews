from django.views.generic.base import View, TemplateResponseMixin
from django.views.generic.edit import CreateView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Permission, ContentType
from django.shortcuts import redirect, reverse
from django.contrib import messages
from .forms import UserCreationFormBlog
from post.models import Post
from album.models import Album, Image


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


def logout_user(request):
    """ Check if the user is already logged out, if not, the user is logged out """
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, 'Usuário deslogado')
        return redirect(reverse('blog:index'))
    else:
        messages.warning(request, 'Usuário já deslogado')
        return redirect(reverse('user:login'))


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
            models_permissions = [Post, Album, Image]
            for model in models_permissions:
                content_type = ContentType.objects.get_for_model(model)
                post_permissions = Permission.objects.filter(content_type=content_type)
                for permission in post_permissions:
                    self.object.user_permissions.add(permission)
        messages.success(self.request, 'Usuário cadastrado')
        return reverse('user:login')
