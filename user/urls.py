from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('cadastrar/', views.Register.as_view(), name='register'),
    path('meus-dados/', views.Update.as_view(), name='update'),
]
