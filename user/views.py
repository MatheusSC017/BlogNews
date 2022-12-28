from django.views.generic.edit import CreateView
from django.contrib.auth import login
from django.contrib.auth.models import User, Permission, ContentType
from django.contrib.auth.views import (
    FormView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
    LoginView,
    LogoutView,
)
from allauth.socialaccount.views import SignupView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, reverse
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import (
    UserCreationFormBlog,
    UserChangeFormBlog,
    AuthenticationFormBlog,
    PasswordResetFormBlog,
    SetPasswordFormBlog,
)
from post.models import Post
from album.models import Album, Image
from search.models import Search, Option
from utils.utils import verify_recaptcha
from allauth.socialaccount import helpers


class Login(LoginView):
    """ Page to user login in the system """
    template_name = 'user/login.html'
    form_class = AuthenticationFormBlog
    redirect_authenticated_user = reverse_lazy('blog:index')

    def get(self, request, *args, **kwargs):
        """ Check if the user is already logged in """
        if request.user.is_authenticated:
            return redirect(reverse('blog:index'))

        return self.render_to_response(self.get_context_data())

    def post(self, request, *args, **kwargs):
        """ Check the user data and login """
        recaptcha_response = request.POST.get('g-recaptcha-response')

        if not verify_recaptcha(recaptcha_response):
            messages.warning(request, 'ReCaptcha inválido')
            return redirect(reverse('user:login'))

        if request.user.is_authenticated:
            messages.warning(request, 'Usuário já logado')
            return redirect(reverse('blog:index'))

        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, 'Usuário logado')
        login(self.request, user=form.get_user())
        return redirect(self.redirect_authenticated_user)


class Logout(LogoutView):
    """ The user is logged out """
    template_name = 'user/logout.html'


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
                permissions = Permission.objects.filter(content_type=content_type)
                for permission in permissions:
                    self.object.user_permissions.add(permission)
        messages.success(self.request, 'Usuário cadastrado')
        return reverse('user:login')


class Update(LoginRequiredMixin, FormView):
    """ Page to update the user data """
    template_name = 'user/update.html'
    model = User
    form_class = UserChangeFormBlog

    def get(self, request, *args, **kwargs):
        """ Include the initial data of the form """
        user_data = {
            'username': request.user.username,
            'email': request.user.email,
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
        }
        self.initial = user_data
        return super().get(request, *args, **kwargs)

    def get_form(self, form_class=None):
        """ Return the form """
        if form_class is None:
            form_class = self.get_form_class()
        return form_class(**self.get_form_kwargs(), instance=self.request.user)

    def form_valid(self, form):
        """ Check if the form is valid """
        form.instance = self.request.user
        form.save()
        messages.success(self.request, "Perfil editado")
        return redirect(reverse('user:update'))


class PasswordReset(PasswordResetView):
    """ Page to inform the email of the user who wants to reset the password """
    email_template_name = 'user/password_reset_email.html'
    template_name = 'user/password_reset.html'
    form_class = PasswordResetFormBlog
    success_url = reverse_lazy('user:password_reset_done')


class PasswordResetDone(PasswordResetDoneView):
    """ Message with instructions """
    template_name = 'user/password_reset_done.html'


class PasswordResetConfirm(PasswordResetConfirmView):
    """ Page that verifies the token and resets the password """
    template_name = 'user/password_reset_confirm.html'
    form_class = SetPasswordFormBlog
    success_url = reverse_lazy('user:password_reset_complete')


class PasswordResetComplete(PasswordResetCompleteView):
    """ Final message to reset the password """
    template_name = 'user/password_reset_complete.html'


class SocialAccountSignupViewBlog(SignupView):
    def form_valid(self, form):
        """ Add the permissions python manage"""
        self.request.session.pop("socialaccount_sociallogin", None)
        user = form.save(self.request)
        if self.request.POST.get('checkpermissions'):
            models_permissions = [Post, Album, Image, Search, Option, ]
            for model in models_permissions:
                content_type = ContentType.objects.get_for_model(model)
                post_permissions = Permission.objects.filter(content_type=content_type)
                for permission in post_permissions:
                    user.user_permissions.add(permission)
        return helpers.complete_social_signup(self.request, self.sociallogin)
