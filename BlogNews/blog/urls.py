from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.Home.as_view(), name='index'),
    path('sobre/', views.about, name='about')
]
