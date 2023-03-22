from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render

from Users.models import User


@login_required(login_url='user-login')
def help_view(request: HttpRequest):
    if request.method == 'POST':
        try:
            subject = request.POST['subject']
            message = request.POST['message']
        except KeyError:
            response = JsonResponse(
                data={
                    'error': 'Invalid data'
                }
            )
            response.status_code = 400
            return response

        user = User.objects.get(username=request.user.username)
        user.help_messages.create(
            subject=subject,
            message=message
        )
        return JsonResponse(
            data={
                'success': True,
                'message': 'Message sent successfully'
            }
        )
    else:
        data = {
            'logged_user': request.user,
            'settings': True,
            'help_center': True,
            'selector': True,
            'new_notifications': request.user.get_new_notifications().count()
        }
        return render(
            request=request,
            template_name='settings-base.html',
            context=data
        )
