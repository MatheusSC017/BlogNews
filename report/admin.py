from django.contrib import admin
from .models import Report


class ReportAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user_report', 'status_report', 'creation_date_report', )
    list_display_links = ('pk', 'user_report', )
    list_filter = ('status_report', )
    search_fields = ('user_report', 'description_report', )


admin.site.register(Report, ReportAdmin)
