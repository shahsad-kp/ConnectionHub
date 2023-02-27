from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from MainUsers.models import User
from utils.helpers import superuser_login_required


@superuser_login_required(login_url='admin-login')
def admin_users(request):
    data = {
        'users': [
            {
                'username': user.username,
                'profile_picture': user.profile_picture.url if user.profile_picture else '',
                'fullname': user.full_name,
                'url': reverse(
                    viewname='admin-profile-pages',
                    args=[
                        user.username
                    ]
                )
            }
            for user in User.objects.all()
        ],
    }
    return render(request, 'admin-users.html', context=data)


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
    username = user.username
    fullname = user.full_name
    profile_picture = user.profile_picture.url if user.profile_picture else ''
    posts = [
        {
            'id': post.id,
            'image': post.image.url,
            'caption': post.caption,
        }
        for post in user.get_posts()
    ]
    bio = user.bio
    email = user.email
    phone_number = user.phone_number
    number_of_followers = len(user.get_all_followers())
    number_of_followings = len(user.get_all_followings())
    context = {
        'username': username,
        'fullname': fullname,
        'profile_picture': profile_picture,
        'bio': bio,
        'posts': posts,
        'email': email,
        'phone_number': phone_number,
        'number_of_followers': number_of_followers,
        'number_of_followings': number_of_followings,
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
