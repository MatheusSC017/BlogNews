from django.forms import ModelForm
from .models import Comment


class CommentForm(ModelForm):
    def clean(self):
        cleaned_data = self.cleaned_data

        comment = cleaned_data.get('comment') or ''

        if len(comment) < 5:
            self.add_error(
                'comment',
                'O comentário deve ter pelo menos 5 caracteres.'
            )

    class Meta:
        model = Comment
        fields = ['comment', ]

    def __init__(self, *args, **kwargs):
        """ Adds design features to the form """
        super().__init__(*args, **kwargs)
        self.fields['comment'].widget.attrs['class'] = 'form-control'
        self.fields['comment'].widget.attrs['placeholder'] = 'Comentário'
