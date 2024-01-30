from django import forms
from .models import Album


class AlbumForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['title'].widget.attrs['placeholder'] = 'Título do álbum'
        self.fields['title'].widget.attrs['class'] = 'form-control'
        self.fields['published'].widget.attrs['class'] = 'form-check-input border border-dark'

    def clean(self, *args, **kwargs):
        title = self.cleaned_data.get('title')
        if len(title) < 5:
            self.add_error(
                'title',
                'O título deve possuir ao menos 5 caracteres'
            )

        return super().clean(*args, **kwargs)

    class Meta:
        model = Album
        fields = ['title', 'published']


class ImageForm(forms.Form):
    image_field = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True,
                                                                          'class': 'form-control',
                                                                          'placeholder': 'Cadastrar imagens'}))
