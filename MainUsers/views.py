from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from AdminReports.models import Report
from MainUsers.models import User, Follow
from utils.posts import get_posts_context
from utils.users import get_suggestion_users_context, get_following_users_context


@login_required(login_url='user-login')
def home_view(request: HttpRequest, username: str):
    logined_user = User.objects.get(pk=request.user.pk)
    user = get_object_or_404(User, username=username)
    username = user.username
    fullname = user.full_name
    profile_picture = user.profile_picture.url
    posts = get_posts_context(user.get_posts(), logined_user)

    bio = user.bio

    context = {
        'username': username,
        'fullname': fullname,
        'profile_picture': profile_picture,
        'bio': bio,
        'posts': posts,
        'number_of_followers': user.followers_count,
        'number_of_followings': user.followings_count,
        'suggestions': get_suggestion_users_context(logined_user),
        'followings': get_following_users_context(logined_user),
        'self': logined_user == user,
    }
    return render(
        request=request,
        template_name='profile-page.html',
        context=context,
    )


@login_required(login_url='user-login')
def search_users(request: HttpRequest):
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
                'profile_picture': user.profile_picture.url,
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


@login_required(login_url='user-login')
def follow_user(request: HttpRequest, username: str):
    user = get_object_or_404(User, username=username)
    org_user = User.objects.get(username=request.user.username)
    if Follow.objects.filter(follower=org_user, followee=user).exists():
        response = JsonResponse(
            {
                'success': False,
                'error': 'Already followed'
            }
        )
        user.save()
        response.status_code = 400
    else:
        org_user.follow(user)
        response = JsonResponse(
            {
                'success': True
            }
        )
    return response


@login_required(login_url='user-login')
def unfollow_user(request: HttpRequest, username: str):
    user = get_object_or_404(User, username=username)
    org_user = User.objects.get(username=request.user.username)
    if Follow.objects.filter(follower=org_user, followee=user).exists():
        org_user.unfollow(user)
        response = JsonResponse(
            {
                'success': True
            }
        )
    else:
        response = JsonResponse(
            {
                'success': False,
                'error': 'Not followed'
            }
        )
        response.status_code = 400
    return response


@login_required(login_url='user-login')
def report_user(request: HttpRequest, username: str):
    user = get_object_or_404(User, username=username)
    org_user = User.objects.get(username=request.user.username)
    if Report.objects.filter(user=user, reported_user=org_user).exists():
        response = JsonResponse(
            data={
                'error': 'Already reported'
            }
        )
        response.status_code = 409
        return response

    report = Report(user=user, reported_user=org_user)
    report.save()
    response = JsonResponse(
        data={
            'success': True
        }
    )
    return response
