from django.urls import path, include
from .views import create_comment, update_comment, delete_comment

app_name = 'comment'

comment_patterns = [
    path('cadastrar/', create_comment, name='comment_create'),
    path('atualizar/', update_comment, name='comment_update'),
    path('delete/', delete_comment, name='comment_delete'),
]

urlpatterns = [
    path('post/<int:post_pk>/', include(comment_patterns))
]
