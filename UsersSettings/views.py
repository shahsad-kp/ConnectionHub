from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render

from Users.models import User
from UsersSettings.models import UserSettings


@login_required(login_url='user-login')
def privacy_settings(request: HttpRequest) -> HttpResponse:
    context = {
        'logged_user': request.user.get_context(),
        'privacy_settings': True,
        'settings': True,
        'private_account': request.user.settings.private_account,
        'blocked_users': [blocks.user.get_context() for blocks in request.user.blocked_users.all()],
        'selector': True,
        'new_notifications': request.user.get_new_notifications().count()
    }
    return render(
        request=request,
        template_name='settings-base.html',
        context=context,
    )


@login_required(login_url='user-login')
def update_user_account_type(request: HttpRequest) -> HttpResponse:
    try:
        new_account_type = request.GET['type']
    except KeyError:
        return JsonResponse(
            data={
                'success': False,
                'error': 'not enough values'
            },
            status=400
        )
    if str(new_account_type).lower() == 'true':
        new_account_type = True
    elif str(new_account_type).lower() == 'false':
        new_account_type = False
    else:
        return JsonResponse(
            data={
                'success': False,
                'error': 'not enough values'
            },
            status=400
        )
    user = User.objects.get(pk=request.user.pk)
    try:
        settings = user.settings
    except User.DoesNotExist:
        settings = UserSettings.objects.create(
            user=user
        )
    settings.private_account = new_account_type
    settings.save()
    return JsonResponse(
        data={
            'success': True,
            'private_account': settings.private_account
        }
    )
