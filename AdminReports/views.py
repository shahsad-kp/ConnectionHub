from django.http import HttpRequest, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from AdminReports.models import Report
from utils.helpers import superuser_login_required


@superuser_login_required(login_url='admin-login')
def admin_report_page(request: HttpRequest):
    reports = Report.objects.all()
    context = {
        'reports': [
            {
                'id': report.id,
                'user': {
                    'username': report.user.username,
                    'profile_picture': report.user.profile_picture.url,
                    'url': reverse(
                        viewname='admin-profile-pages',
                        args=[
                            report.user.username
                        ]
                    )
                },
                'reported_user': {
                    'username': report.reported_user.username,
                    'profile_picture': report.reported_user.profile_picture.url,
                    'url': reverse(
                        viewname='admin-profile-pages',
                        args=[
                            report.reported_user.username
                        ]
                    )
                },
                'date_created': report.date_created,
            }
            for report in reports
        ],
        'number_of_reports': reports.count()
    }
    return render(request, 'admin_report_page.html', context=context)


@superuser_login_required(login_url='admin-login')
def admin_report_handled(request: HttpRequest, report_id: int):
    report = get_object_or_404(Report, id=report_id)
    report.handled = True
    report.save()
    return JsonResponse(
        data={
            'success': True,
        }
    )
