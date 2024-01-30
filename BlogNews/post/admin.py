from django.contrib import admin
from django_summernote import admin as summer_admin
from .models import Post, Category, RattingUserPost


class PostAdmin(summer_admin.SummernoteModelAdmin):
    list_display = ('id', 'title', 'user', 'published', 'publication_date',
                    'edition_date', 'album', 'category',)
    list_display_links = ('id', 'title',)
    list_filter = ('published', 'category',)
    list_editable = ('published',)
    search_fields = ('title', 'album',)
    ordering = ('edition_date', 'publication_date',)
    list_per_page = 50
    summernote_fields = ('description',)


admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(RattingUserPost)
