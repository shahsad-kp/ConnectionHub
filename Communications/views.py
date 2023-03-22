from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render

from Communications.models import Message
from Users.models import User


@login_required(login_url='user-login')
def chat_list(request, username=None):
    if 'q' in request.GET and request.GET['q']:
        search = request.GET['q']
        users = User.not_blocked_users(logined_user=request.user).filter(username__icontains=search, is_banned=False)

    else:
        messages = Message.not_blocked_messages(request.user).filter(
            Q(sender=request.user) |
            Q(receiver=request.user)
        ).order_by('-timestamp')
        users = [
            message.sender if message.sender != request.user else message.receiver
            for message in messages
        ]

    # remove duplicates without changing the order
    interacted_users = []

    for user in users:
        if user.get_context() not in [i['user'] for i in interacted_users]:
            interacted_users.append(
                {
                    'user': user.get_context(),
                    'unviewed_messages': Message.not_blocked_messages(request.user).filter(
                        sender=user, receiver=request.user, viewed=False
                    ).exists()
                }
            )

    context = {
        'logged_user': request.user.get_context(),
        'interacted_users': interacted_users,
        'new_notifications': request.user.get_new_notifications().count()
    }
    if username:
        try:
            selected_user = User.not_blocked_users(logined_user=request.user).get(username=username)
            Message.objects.filter(
                sender=selected_user, receiver=request.user, viewed=False
            ).update(viewed=True)
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
