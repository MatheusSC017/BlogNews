from django import forms
from django.forms import DateTimeInput
from .models import Search, Option


class SearchForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in ['description_search', 'publication_date_search', 'finish_date_search', ]:
            self.fields[field].widget.attrs['class'] = 'form-control'
            self.fields[field].widget.attrs['placeholder'] = self.fields[field].label
        self.fields['published_search'].widget.attrs['class'] = 'form-check-input'

    class Meta:
        model = Search
        fields = ['description_search', 'publication_date_search', 'finish_date_search', 'published_search']


class OptionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['response_option'].widget.attrs['class'] = 'form-control'
        self.fields['response_option'].widget.attrs['placeholder'] = self.fields['response_option'].label

    class Meta:
        fields = ['pk', 'response_option', 'search_option']


OptionInlineForm = forms.inlineformset_factory(Search,
                                               Option,
                                               OptionForm,
                                               extra=6,
                                               fields=['response_option', ],
                                               min_num=2,
                                               max_num=8,
                                               can_delete_extra=True)
