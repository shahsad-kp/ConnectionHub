from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from Admin.helpers import superuser_login_required
from Users.models import User


@superuser_login_required(login_url='admin-login')
def admin_users(request):
    data = {
        'users': [
            user.get_context()
            for user in User.objects.all().order_by('-date_joined')
        ],
    }
    return render(
        request=request,
        template_name='admin-users.html',
        context=data
    )


@superuser_login_required(login_url='admin-login')
def admin_search_users(request):
    if not ((request.method == 'GET') & ('q' in request.GET)):
        response = JsonResponse(
            data={
                'error': 'Invalid parameter'
            }
        )
        response.status_code = 401
        return response

    query = request.GET['q']
    results = User.objects.filter(username__icontains=query)
    data = {
        'results': [
            {
                'username': user.username,
                'fullname': user.full_name,
                'profile_url': user.profile_picture.url if user.profile_picture else '',
                'url': reverse(
                    viewname='profile-pages',
                    args=[
                        user.username
                    ]
                )
            }
            for user in results
        ],
        'number_of_results': results.count()
    }
    return JsonResponse(
        data=data
    )


@superuser_login_required(login_url='admin-login')
def admin_profile_pages(request, username):
    user = get_object_or_404(User, username=username)
    context = {
        'user': user.get_context(admin_data=True, posts=True)
    }
    return render(
        request=request,
        template_name='admin-profile-page.html',
        context=context,
    )


@superuser_login_required(login_url='admin-login')
def admin_profile_delete(request, username):
    user = get_object_or_404(User, username=username)
    user.delete()
    return redirect('admin-users')