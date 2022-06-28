from django.forms import models


class SearchForm(models.ModelForm):
    class Meta:
        fields = ['description_search', 'publication_date_search', 'finish_date_search', 'published_search', ]


class OptionForm(models.BaseInlineFormSet):
    class Meta:
        fields = ['response_option', 'vote_option']
