from django.views.generic.base import View, TemplateResponseMixin
from django.views.generic.edit import CreateView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import redirect, reverse
from django.contrib import messages
from .forms import UserCreationFormBlog


class Login(View, TemplateResponseMixin):
    template_name = 'user/login.html'

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            messages.warning(self.request, 'Usuário já logado')
            return redirect(reverse('blog:index'))

        return self.render_to_response({})

    def post(self, *args, **kwargs):
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
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, 'Usuário deslogado')
        return redirect(reverse('blog:index'))
    else:
        messages.warning(request, 'Usuário já deslogado')
        return redirect(reverse('user:login'))


class Register(CreateView):
    template_name = 'user/register.html'
    model = User
    form_class = UserCreationFormBlog

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse('blog:index'))

        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        messages.success(self.request, 'Usuário cadastrado')
        return reverse('user:login')
