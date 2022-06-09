from django.views.generic.base import View, TemplateResponseMixin
from django.views.generic.edit import BaseCreateView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, reverse
from django.contrib import messages


class Home(View):
    pass


class Login(View, TemplateResponseMixin):
    template_name = 'user/login.html'

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect(reverse('user:index'))

        return self.render_to_response({})

    def post(self, *args, **kwargs):
        username = self.request.POST.get('username')
        password = self.request.POST.get('password')

        if self.request.user.is_authenticated:
            return redirect(reverse('user:index'))

        user = authenticate(self.request, username=username, password=password)
        if user is not None:
            login(self.request, user=user)
            messages.success(self.request, 'Usuário logado')
            return redirect(reverse('user:index'))
        else:
            messages.error(self.request, 'Usuário ou senha incorretos.')
            return self.render_to_response({})


def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, 'Usuário deslogado')
        return redirect(reverse('user:index'))
    else:
        messages.warning(request, 'Usuário já deslogado')
        return redirect(reverse('user:login'))


class Register(BaseCreateView, TemplateResponseMixin):
    template_name = 'user/register.html'

    def get(self, *args, **kwargs):
        self.render_to_response({})
