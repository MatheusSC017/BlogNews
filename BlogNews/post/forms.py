from django.forms import ModelForm
from django_summernote.widgets import SummernoteWidget
from .models import Post


class PostForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        format_fields = ['title', 'excerpt', 'image', 'publication_date', 'edition_date', ]
        for field in format_fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
            self.fields[field].widget.attrs['placeholder'] = self.fields[field].label
        self.fields['category'].widget.attrs['class'] = 'form-select'
        self.fields['album'].widget.attrs['class'] = 'form-select'
        self.fields['publication_date'].disabled = True
        self.fields['edition_date'].disabled = True

    def clean(self):
        cleaned_data = self.cleaned_data

        if len(cleaned_data['title']) < 5:
            self.add_error(
                'title',
                'O título deve possuir ao menos 5 caracteres.'
            )

        if len(cleaned_data['excerpt']) < 20:
            self.add_error(
                'excerpt',
                'O excerto deve possuir ao menos 20 caracteres.'
            )

        if len(cleaned_data['description']) < 20:
            self.add_error(
                'description',
                'A descrição deve possuir ao menos 20 caracteres.'
            )

        return super().clean()

    class Meta:
        model = Post
        fields = ['title', 'excerpt', 'description', 'image',
                  'category', 'album', 'publication_date', 'edition_date', ]
        widgets = {
            'description': SummernoteWidget(),
        }
