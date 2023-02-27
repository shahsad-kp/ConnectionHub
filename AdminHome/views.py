from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse, HttpRequest
from django.shortcuts import render, redirect

from AdminMessages.models import HelpMessage
from AdminReports.models import Report
from MainPosts.models import Post, Comment
from MainUsers.models import User
from utils.helpers import superuser_login_required


@superuser_login_required(login_url='admin-login')
def admin_home(request):
    data = {
        'users': User.objects.all().count(),
        'posts': Post.objects.all().count(),
        'reports': Report.objects.all().count(),
        'messages': HelpMessage.objects.all().count(),
        'comments': Comment.objects.all().count()
    }
    return render(request, 'admin-home.html', context=data)


def admin_login(request):
    if request.method == 'POST':
        try:
            username = request.POST['username']
            password = request.POST['password']
        except KeyError:
            response = JsonResponse(
                data={
                    'error': 'Invalid data'
                }
            )
            response.status_code = 400
            return response
        user = authenticate(request, username=username, password=password)
        if (user is not None) and user.is_superuser:
            login(request, user)
            return redirect('admin-home')
        else:
            response = JsonResponse(
                data={
                    'error': 'Invalid username or password'
                }
            )
            response.status_code = 400
            return response
    return render(request, 'admin-login.html')


@superuser_login_required(login_url='admin-login')
def admin_logout(request: HttpRequest):
    logout(request)
    return redirect(
        to='admin-login'
    )
