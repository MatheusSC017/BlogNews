from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    path('', views.Home.as_view(), name='index'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.Register.as_view(), name='register'),
]
