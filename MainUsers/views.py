from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from AdminReports.models import Report
from MainUsers.models import User, Follow


@login_required(login_url='user-login')
def home_view(request: HttpRequest, username: str):
    user = get_object_or_404(User, username=username)
    username = user.username
    fullname = user.full_name
    profile_picture = user.profile_picture
    posts = user.get_posts()
    bio = user.bio
    number_of_followers = len(user.get_all_followers())
    number_of_followings = len(user.get_all_followings())
    context = {
        'username': username,
        'fullname': fullname,
        'profile_picture': profile_picture,
        'bio': bio,
        'posts': posts,
        'number_of_followers': number_of_followers,
        'number_of_followings': number_of_followings,
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


def check_username_availability(request: HttpRequest):
    if not ((request.method == 'GET') & ('q' in request.GET)):
        response = JsonResponse(
            data={
                'error': 'Invalid parameter'
            }
        )
        response.status_code = 401
        return response

    query = request.GET['q']
    if User.objects.filter(username=query).exists():
        response = JsonResponse(
            data={
                'available': False
            }
        )
    else:
        response = JsonResponse(
            data={
                'available': True
            }
        )
    return response


def check_email_availability(request: HttpRequest):
    if not ((request.method == 'GET') & ('q' in request.GET)):
        response = JsonResponse(
            data={
                'error': 'Invalid parameter'
            }
        )
        response.status_code = 401
        return response

    query = request.GET['q']
    if User.objects.filter(email=query).exists():
        response = JsonResponse(
            data={
                'available': False
            }
        )
    else:
        response = JsonResponse(
            data={
                'available': True
            }
        )
    return response
