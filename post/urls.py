from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.Blog.as_view(), name='blog'),
    path('<int:pk>/', views.Post.as_view(), name='post'),
]