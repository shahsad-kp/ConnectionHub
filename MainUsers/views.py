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

    context = {
        'user': user.get_context(logined_user, True),
        'suggestions': get_suggestion_users_context(logined_user),
        'followings': get_following_users_context(logined_user),
        'logged_user': request.user.get_context()
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
                'success': True,
                'followed': True,
                'followers': user.followers_count,
                'followings': user.followings_count,
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
                'success': True,
                'followed': False,
                'followers': user.followers_count,
                'followings': user.followings_count,
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
    if request.method == 'POST':
        if Report.objects.filter(user=user, reported_user=org_user).exists():
            response = JsonResponse(
                data={
                    'error': 'Already reported'
                }
            )
            response.status_code = 409
            return response
        elif user == org_user:
            response = JsonResponse(
                data={
                    'error': 'Cannot report yourself'
                }
            )
            response.status_code = 409
            return response
        elif 'reason' not in request.POST:
            response = JsonResponse(
                data={
                    'error': 'Invalid parameter'
                }
            )
            response.status_code = 401
            return response

        reason = request.POST['reason']
        report = Report(
            user=user,
            reported_user=org_user,
            reason=reason
        )
        report.save()
        response = JsonResponse(
            data={
                'success': True
            }
        )
        return response
    else:
        response = JsonResponse(
            data={
                'error': 'Invalid method'
            }
        )
        response.status_code = 405
        return response
