from django.contrib import admin
from .models import Report
from user.models import UserReportRegister


class ReportAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user_report', 'status_report', 'creation_date_report', )
    list_display_links = ('pk', 'user_report', )
    list_filter = ('status_report', )
    search_fields = ('user_report', 'description_report', )
    exclude = ('status_report', )
    actions = ('approve_report', 'reject_report', )

    @admin.action(description='Aprovar denúncia de usúario')
    def approve_report(self, request, queryset):
        for report in queryset:
            if report.status_report != 'w':
                continue

            report.status_report = 'a'
            report.save()

            if report.user_report.is_staff:
                continue

            if not hasattr(report.user_report, 'userreportregister'):
                user_report_register = UserReportRegister.objects.create(user_userreportregister=report.user_report)
            else:
                user_report_register = report.user_report.userreportregister

            user_report_register.reports_userreportregister += 1

            if user_report_register.reports_userreportregister >= 3:
                user_report_register.status_userreportregister = 'b'
                report.user_report.user_permissions.clear()

            user_report_register.save()

    @admin.action(description='Rejeitar denúncia de usuário')
    def reject_report(self, request, queryset):
        for report in queryset:
            if report.status_report != 'w':
                continue

            report.status_report = 'r'
            report.save()


admin.site.register(Report, ReportAdmin)
