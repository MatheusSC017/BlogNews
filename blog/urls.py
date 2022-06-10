from django.urls import path
from .views import Home

app_name = 'blog'

urlpatterns = [
    path('', Home.as_view(), name='index'),
]