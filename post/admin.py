from django.contrib import admin
from django_summernote import admin as summer_admin
from .models import Post, Category, RattingUserPost

class PostAdmin(summer_admin.SummernoteModelAdmin):
    list_display = ('id', 'title_post', 'ratting_post', 'published_post',
                    'published_date_post', 'edition_date_post', 'album_post', 'category_post',)
    list_display_links = ('id', 'title_post',)
    list_filter = ('published_post', 'category_post',)
    list_editable = ('published_post',)
    search_fields = ('title_post', 'album_post',)
    ordering = ('edition_date_post', 'published_date_post', 'ratting_post',)
    list_per_page = 30
    summernote_fields = ('description_post',)


admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(RattingUserPost)
