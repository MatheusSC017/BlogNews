from django.test import TestCase
from django.shortcuts import reverse
from django.http import HttpRequest
from django.contrib.auth.models import User
from django.utils import lorem_ipsum
from .models import Report
from user.models import UserReportRegister


class ReportActionsTestCase(TestCase):
    def setUp(self):
        self.client = self.client_class()

        self.admin = User.objects.create_superuser(username='admin', email='admin@admin.com', password='admin123456')
        self.user = User.objects.create_user(username='username_test', email='email@test.com', password='password_test')
        self.report = Report.objects.create(user=self.user, description=lorem_ipsum.paragraph())

    def test_approve_report(self):
        self.client.login(username='admin', password='admin123456', request=HttpRequest())
        response = self.client.post(reverse('admin:report_report_changelist'), {
            'action': 'approve_report',
            '_selected_action': [self.report.pk, ]
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('admin:report_report_changelist'))
        report = Report.objects.get(pk=self.report.pk)
        self.assertEqual(report.status, 'a')
        user = User.objects.get_by_natural_key(self.user.username)
        self.assertEqual(user.userreportregister.reports, 1)

    def test_approve_report_user_with_3_reports(self):
        UserReportRegister.objects.create(user=self.user,
                                          reports=2)
        self.client.login(username='admin', password='admin123456', request=HttpRequest())
        response = self.client.post(reverse('admin:report_report_changelist'), {
            'action': 'approve_report',
            '_selected_action': [self.report.pk, ]
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('admin:report_report_changelist'))
        report = Report.objects.get(pk=self.report.pk)
        self.assertEqual(report.status, 'a')
        user = User.objects.get_by_natural_key(self.user.username)
        self.assertEqual(user.userreportregister.reports, 3)
        self.assertEqual(user.userreportregister.status, 'b')

    def test_reject_report(self):
        self.client.login(username='admin', password='admin123456', request=HttpRequest())
        response = self.client.post(reverse('admin:report_report_changelist'), {
            'action': 'reject_report',
            '_selected_action': [self.report.pk, ]
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('admin:report_report_changelist'))
        report = Report.objects.get(pk=self.report.pk)
        self.assertEqual(report.status, 'r')
