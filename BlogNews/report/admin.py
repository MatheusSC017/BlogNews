from django.contrib import admin
from .models import Report
from user.models import UserReportRegister


class ReportAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'status', 'creation_date', )
    list_display_links = ('pk', 'user', )
    list_filter = ('status', )
    search_fields = ('user', 'description', )
    exclude = ('status', )
    actions = ('approve_report', 'reject_report', )

    @admin.action(description='Aprovar denúncia de usúario')
    def approve_report(self, request, queryset):
        for report in queryset:
            if report.status != 'w':
                continue

            report.status = 'a'
            report.save()

            if report.user.is_staff:
                continue

            if not hasattr(report.user, 'userreportregister'):
                user_report_register = UserReportRegister.objects.create(user=report.user)
            else:
                user_report_register = report.user.userreportregister

            user_report_register.reports += 1

            if user_report_register.reports >= 3:
                user_report_register.status = 'b'
                report.user.user_permissions.clear()

            user_report_register.save()

    @admin.action(description='Rejeitar denúncia de usuário')
    def reject_report(self, request, queryset):
        for report in queryset:
            if report.status != 'w':
                continue

            report.status = 'r'
            report.save()


admin.site.register(Report, ReportAdmin)
