from django.urls import path, include
from . import views

app_name = 'search'

search_patterns = [
    path('', views.UserSearches.as_view(), name='user_search'),
    path('cadastrar/', views.CreateSearch.as_view(), name='search_create'),
]

urlpatterns = [
    path('minhas_pesquisas/', include(search_patterns))
]
