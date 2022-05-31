from django.urls import path
from . import views

urlpatterns = [
    path('', views.Blog.as_view, name='blog'),
]