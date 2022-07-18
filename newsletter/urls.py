from django.urls import path
from . import views

app_name = 'newsletter'

urlpatterns = [
    path('', views.newsletter_add_user, name='add_user'),
    path('agradecimento/', views.done_newsletter_add_user, name='done_add_user'),
    path('cancelar/', views.UnsubscribeNewsletter.as_view(), name='unsubscribe'),
    path('desculpas/', views.DoneUnsubscribeNewsletter.as_view(), name='unsubscribe_done'),
    path('confirmar_cancelamento/<token>', views.ConfirmUnsubscribeNewsletter.as_view(), name='unsubscribe_confirm'),
    path('finalizacao/', views.FinishUnsubscribeNewsletter.as_view(), name='unsubscribe_finish'),
]
