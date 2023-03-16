from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render

from Communications.models import Message
from Users.models import User


@login_required(login_url='user-login')
def chat_list(request, username=None):
    if 'q' in request.GET and request.GET['q']:
        search = request.GET['q']
        users = User.objects.filter(username__icontains=search)
    else:
        users = request.user.get_all_followings()

    context = {
        'logged_user': request.user.get_context(),
        'users_followed': [user.get_context() for user in users],
    }
    if username:
        try:
            selected_user = User.objects.get(username=username)
            messages = Message.objects.filter(
                Q(sender=request.user, receiver=selected_user) |
                Q(sender=selected_user, receiver=request.user)
            ).order_by('timestamp')
            context['selected_user'] = selected_user.get_context(request.user)
            context['messages'] = [
                message.get_context(request.user)
                for message in messages
            ]
        except User.DoesNotExist:
            context['selected_user'] = None
    return render(
        request=request,
        template_name='chat-list.html',
        context=context
    )
