from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, JsonResponse
from django.shortcuts import get_object_or_404

from Reports.models import Report
from Users.models import User


@login_required(login_url='user-login')
def report_user(request: HttpRequest, username: str):
    org_user = User.objects.get(username=request.user.username)
    user = get_object_or_404(User.not_blocked_users(org_user), username=username)
    if request.method == 'POST':
        if Report.objects.filter(user=user, reported_user=org_user).exists():
            response = JsonResponse(
                data={
                    'error': 'Already reported'
                }
            )
            response.status_code = 409
            return response
        elif user == org_user:
            response = JsonResponse(
                data={
                    'error': 'Cannot report yourself'
                }
            )
            response.status_code = 409
            return response
        elif 'reason' not in request.POST:
            response = JsonResponse(
                data={
                    'error': 'Invalid parameter'
                }
            )
            response.status_code = 401
            return response

        reason = request.POST['reason']
        report = Report(
            user=user,
            reported_user=org_user,
            reason=reason
        )
        report.save()
        response = JsonResponse(
            data={
                'success': True
            }
        )
        return response
    else:
        response = JsonResponse(
            data={
                'error': 'Invalid method'
            }
        )
        response.status_code = 405
        return response
