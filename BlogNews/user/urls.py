from django.urls import path, include
from . import views

app_name = 'user'

reset_password_patterns = [
    path('', views.PasswordReset.as_view(), name='password_reset'),
    path('enviar/', views.PasswordResetDone.as_view(), name='password_reset_done'),
    path('<uidb64>/<token>/', views.PasswordResetConfirm.as_view(), name='password_reset_confirm'),
    path('redefir/', views.PasswordResetComplete.as_view(), name='password_reset_complete'),
]

urlpatterns = [
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('cadastrar/', views.Register.as_view(), name='register'),
    path('meus-dados/', views.Update.as_view(), name='update'),
    path('resetar-senha/', include(reset_password_patterns)),
]
