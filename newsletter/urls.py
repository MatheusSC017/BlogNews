from django.urls import path
from .views import newsletter_add_user, done_newsletter_add_user

app_name = 'newsletter'

urlpatterns = [
    path('', newsletter_add_user, name='add_user'),
    path('agradecimento/', done_newsletter_add_user, name='done_add_user')
]
