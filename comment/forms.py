from django.forms import ModelForm
from .models import Comment


class MessageForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['comment',]
