from django import forms
from .models import Search, Option


class SearchForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in ['description', 'publication_date', 'finish_date', ]:
            self.fields[field].widget.attrs['class'] = 'form-control'
            self.fields[field].widget.attrs['placeholder'] = self.fields[field].label
        self.fields['published'].widget.attrs['class'] = 'form-check-input'

    class Meta:
        model = Search
        fields = ['description', 'publication_date', 'finish_date', 'published']


class OptionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['response'].widget.attrs['class'] = 'form-control'
        self.fields['response'].widget.attrs['placeholder'] = self.fields['response'].label

    class Meta:
        fields = ['pk', 'response', 'search']


OptionInlineForm = forms.inlineformset_factory(Search,
                                               Option,
                                               OptionForm,
                                               extra=6,
                                               fields=['response', ],
                                               min_num=2,
                                               max_num=8,
                                               can_delete_extra=True)
