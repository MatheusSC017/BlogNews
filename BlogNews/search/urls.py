from django.urls import path, include
from . import views

app_name = 'search'

search_patterns = [
    path('', views.UserSearches.as_view(), name='user_search'),
    path('cadastrar/', views.CreateSearch.as_view(), name='search_create'),
    path('atualizar/<int:pk>/', views.UpdateSearch.as_view(), name='search_update'),
    path('deletar/', views.delete_search, name='search_delete'),
]

urlpatterns = [
    path('minhas_pesquisas/', include(search_patterns)),
    path('', views.Searches.as_view(), name='searches'),
    path('<int:pk>/', views.Search.as_view(), name='search'),
    path('denunciar/', views.register_report, name='report'),
]
