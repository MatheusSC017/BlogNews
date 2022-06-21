from django.urls import path, include
from .views import Album, AlbumUser

app_name = 'album'

user_patterns = [
    path('', AlbumUser.as_view(), name='user_album')
]

urlpatterns = [
    path('', Album.as_view(), name='album'),
    path('usuario/', include(user_patterns)),
]
