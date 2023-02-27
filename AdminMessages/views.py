from django.http import HttpRequest
from django.shortcuts import render
from django.urls import reverse

from AdminMessages.models import HelpMessage
from utils.helpers import superuser_login_required


@superuser_login_required(login_url='admin-login')
def admin_messages_page(request: HttpRequest):
    messages = HelpMessage.objects.all()
    data = {
        'messages': [
            {
                'id': message.id,
                'user': {
                    'username': message.user.username,
                    'profile_picture': message.user.profile_picture.url,
                    'url': reverse(
                        viewname='admin-profile-pages',
                        args=[
                            message.user.username
                        ]
                    )
                },
                'subject': message.subject,
                'message': message.message,
                'date_created': message.date_created,
            }
            for message in messages
        ]
    }

    return render(request, 'admin_messages_page.html', context=data)
