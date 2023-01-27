from django.contrib import admin
from .models import Search, Option, VottingUserOption


class OptionInlineAdmin(admin.TabularInline):
    model = Option
    min_num = 2
    max_num = 8
    verbose_name = 'alternativa'


class SearchAdmin(admin.ModelAdmin):
    list_display = ['pk', 'user_search', 'publication_date_search', 'finish_date_search', 'published_search', ]
    list_display_links = ['pk', 'user_search', ]
    list_filter = ['published_search', ]
    list_editable = ['published_search', ]
    ordering = ['publication_date_search', 'finish_date_search', ]
    search_fields = ['description_search', ]
    list_per_page = 50
    inlines = [OptionInlineAdmin, ]


admin.site.register(Search, SearchAdmin)
admin.site.register(VottingUserOption)
