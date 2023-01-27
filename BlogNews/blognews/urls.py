"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from user.views import SocialAccountSignupViewBlog
from allauth.socialaccount.views import ConnectionsView, LoginCancelledView, LoginErrorView

allauth_patterns = [
    path('social/cadastrar/', SocialAccountSignupViewBlog.as_view(), name='socialaccount_signup'),
    path('social/conexoes/', ConnectionsView.as_view(), name='socialaccount_connections'),
    path('social/login/cancelar/', LoginCancelledView.as_view(), name='socialaccount_login_cancelled'),
    path('social/login/erro/', LoginErrorView.as_view(), name='socialaccount_login_error'),
    path('', include('allauth.socialaccount.providers.google.urls')),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
    path('usuario/', include('user.urls')),
    path('post/', include('post.urls')),
    path('comentario/', include('comment.urls')),
    path('album/', include('album.urls')),
    path('pesquisa/', include('search.urls')),
    path('newsletter/', include('newsletter.urls')),
    path('summernote/', include('django_summernote.urls')),
    path('contas/', include(allauth_patterns)),

    # TODO: Remover no final do projeto
    path('__debug__/', include('debug_toolbar.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
