from django.forms import ModelForm
from .models import Comment


class CommentForm(ModelForm):
    def clean(self):
        cleaned_data = self.cleaned_data

        comment = cleaned_data.get('comment')

        if len(comment) < 5:
            self.add_error(
                'comment',
                'O comentário deve ter pelo menos 5 caracteres.'
            )

        return super().clean(self)

    class Meta:
        model = Comment
        fields = ['comment', ]
