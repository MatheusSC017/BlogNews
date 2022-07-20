from django.urls import path, include
from . import views

app_name = 'post'

post_patterns = [
    path('', views.BlogUser.as_view(), name='user_blog'),
    path('cadastrar/', views.RegisterPost.as_view(), name='post_create'),
    path('atualizar/<int:pk>/', views.UpdatePost.as_view(), name='post_update'),
]

urlpatterns = [
    path('', views.Blog.as_view(), name='blog'),
    path('<int:pk>/', views.Post.as_view(), name='post'),
    path('meus_posts/', include(post_patterns)),
    path('denunciar/', views.register_report, name='report')
]
