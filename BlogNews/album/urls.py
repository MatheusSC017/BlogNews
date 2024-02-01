from django.urls import path, include
from . import views

app_name = 'album'

albuns_patterns = [
    path('', views.AlbumUser.as_view(), name='user_album'),
    path('cadastrar/', views.AlbumCreate.as_view(), name='album_create'),
    path('atualizar/', views.album_update, name='album_update'),
    path('deletar/', views.album_delete, name='album_delete'),
    path('<int:pk>/', views.AlbumImagesUser.as_view(), name='user_images'),
    path('<int:pk>/cadastrar/', views.UploadImages.as_view(), name='images_create'),
    path('<int:pk>/atualizar/', views.image_update_title, name='image_update'),
    path('<int:pk>/deletar/', views.image_delete, name='image_delete'),
    path('<int:pk>/deletar/imagens/', views.multiple_image_delete, name='images_delete'),
]

urlpatterns = [
    path('', views.Album.as_view(), name='album'),
    path('load_more/', views.load_more_albuns, name='load_more_content'),
    path('<int:pk>/', views.AlbumImages.as_view(), name='image'),
    path('meus_albuns/', include(albuns_patterns)),
    path('reportar/', views.register_report, name='report'),
]
