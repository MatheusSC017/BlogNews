from django.urls import path
from . import views

app_name = 'album'

urlpatterns = [
    path('', views.Album.as_view(), name='album'),
    path('meus_albuns/', views.AlbumUser.as_view(), name='user_album'),
    path('cadastrar/', views.AlbumCreate.as_view(), name='album_create'),
    path('atualizar/', views.album_update, name='album_update'),
    path('deletar/<int:pk>/', views.AlbumDelete.as_view(), name='album_delete'),
]
