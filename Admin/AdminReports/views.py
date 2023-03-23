from django.http import HttpRequest, JsonResponse
from django.shortcuts import render, get_object_or_404

from Admin.helpers import superuser_login_required
from Reports.models import Report


@superuser_login_required(login_url='admin-login')
def admin_report_page(request: HttpRequest):
    reports = Report.objects.all().order_by('-date_created')
    context = {
        'reports': [
            report.get_context()
            for report in reports
        ]
    }
    return render(request, 'admin-report-page.html', context=context)


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
