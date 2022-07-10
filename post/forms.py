from django.forms import ModelForm
from django_summernote.widgets import SummernoteWidget
from .models import Post


class PostForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        format_fields = ['title_post', 'excerpt_post', 'image_post', 'publication_date_post', 'edition_date_post', ]
        for field in format_fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
            self.fields[field].widget.attrs['placeholder'] = self.fields[field].label
        self.fields['category_post'].widget.attrs['class'] = 'form-select'
        self.fields['publication_date_post'].disabled = True
        self.fields['edition_date_post'].disabled = True

    def clean(self):
        cleaned_data = self.cleaned_data

        if len(cleaned_data['title_post']) < 5:
            self.add_error(
                'title_post',
                'O título deve possuir ao menos 5 caracteres.'
            )

        if len(cleaned_data['excerpt_post']) < 20:
            self.add_error(
                'excerpt_post',
                'O excerto deve possuir ao menos 20 caracteres.'
            )

        if len(cleaned_data['description_post']) < 20:
            self.add_error(
                'description_post',
                'A descrição deve possuir ao menos 20 caracteres.'
            )

        return super().clean()

    class Meta:
        model = Post
        fields = ['title_post', 'excerpt_post', 'description_post', 'image_post',
                  'category_post', 'publication_date_post', 'edition_date_post', ]
        widgets = {
            'description_post': SummernoteWidget(),
        }
