from django.contrib import admin
from .models import UserReportRegister


class UserReportRegisterAdmin(admin.ModelAdmin):
    list_display = ['user_userreportregister', 'reports_userreportregister', 'status_userreportregister', ]
    list_display_links = ['user_userreportregister', ]
    list_filter = ['status_userreportregister', ]
    search_fields = ['user_userreportregister', ]


admin.site.register(UserReportRegister, UserReportRegisterAdmin)
