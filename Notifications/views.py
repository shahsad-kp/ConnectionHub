from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from .models import Notification


@login_required(login_url='user-login')
def notification_view(request):
    notifications = Notification.objects.filter(
        recipient=request.user
    ).order_by('-timestamp')
    follow_requests = request.user.follow_requests.all().order_by('-created_at')
    context = {
        'notifications': [
            notification.get_context()
            for notification in notifications
        ],
        'requests': [
            follow_request.get_context(request.user)
            for follow_request in follow_requests
        ],
        'logged_user': request.user.get_context(),
        'notification_tab': True,
    }
    return render(
        request=request,
        template_name='notification-page.html',
        context=context
    )


@login_required(login_url='user-login')
def mark_as_viewed(request, notification_id):
    notification = Notification.objects.get(id=notification_id)
    notification.viewed = True
    notification.save()
    return JsonResponse(
        data={
            'success': True,
        }
    )
