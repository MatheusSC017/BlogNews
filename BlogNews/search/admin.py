from django.contrib import admin
from .models import Search, Option, VottingUserOption


class OptionInlineAdmin(admin.TabularInline):
    model = Option
    min_num = 2
    max_num = 8
    verbose_name = 'alternativa'


class SearchAdmin(admin.ModelAdmin):
    list_display = ['pk', 'user', 'publication_date', 'finish_date', 'published', ]
    list_display_links = ['pk', 'user', ]
    list_filter = ['published', ]
    list_editable = ['published', ]
    ordering = ['publication_date', 'finish_date', ]
    search_fields = ['description', ]
    list_per_page = 50
    inlines = [OptionInlineAdmin, ]


admin.site.register(Search, SearchAdmin)
admin.site.register(VottingUserOption)
