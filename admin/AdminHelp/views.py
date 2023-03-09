from django.http import HttpRequest
from django.shortcuts import render

from Admin.helpers import superuser_login_required
from Help.models import HelpMessage


@superuser_login_required(login_url='admin-login')
def admin_messages_page(request: HttpRequest):
    messages = HelpMessage.objects.all()
    data = {
        'messages': [
            message.get_context()
            for message in messages
        ]
    }

    return render(request, 'admin-messages-page.html', context=data)
