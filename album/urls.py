from django.urls import path, include
from . import views

app_name = 'album'

albuns_patterns = [
    path('', views.AlbumUser.as_view(), name='user_album'),
    path('cadastrar/', views.AlbumCreate.as_view(), name='album_create'),
    path('atualizar/', views.album_update, name='album_update'),
    path('deletar/', views.album_delete, name='album_delete'),
    path('<int:pk>/', views.AlbumImagesUser.as_view(), name='user_images'),
    path('<int:pk>/cadastrar/', views.UploadImages.as_view(), name='images_create')
]

urlpatterns = [
    path('', views.Album.as_view(), name='album'),
    path('meus_albuns/', include(albuns_patterns)),
]
