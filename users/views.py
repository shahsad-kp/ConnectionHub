from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from .models import User, Follow


@login_required(login_url='user-login')
def home_view(request: HttpRequest, username: str):
    logined_user = User.objects.get(pk=request.user.pk)
    user = get_object_or_404(User, username=username)

    context = {
        'user': user.get_context(logined_user, True),
        'suggestions': [
            user.get_context(logined_user)
            for user in logined_user.get_suggestions()
        ],
        'followings': [
            user.get_context(logined_user)
            for user in logined_user.get_all_followings()
        ],
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
def settings_update_profile(request: HttpRequest):
    if request.method == 'POST':
        try:
            username = request.POST['username']
            fullname = request.POST['fullname']
            email = request.POST['email']
            bio = request.POST['bio']
            phone_number = request.POST['phone']
            profile_picture = request.FILES.get('profile-picture')
        except KeyError:
            response = JsonResponse(
                data={
                    'error': 'Invalid data'
                }
            )
            response.status_code = 400
            return response
        user = User.objects.get(username=request.user.username)
        if username:
            if (user.username != username) and (User.objects.filter(username__iexact=username).exists()):
                response = JsonResponse(
                    data={
                        'error': 'Username is not available'
                    }
                )
                response.status_code = 409
                return response

            user.username = username

        if profile_picture:
            user.profile_picture = profile_picture

        if fullname:
            user.full_name = fullname
        if email:
            if (user.email != email) and (User.objects.filter(email__iexact=email).exists()):
                response = JsonResponse(
                    data={
                        'error': 'Email is already connected to another account'
                    }
                )
                response.status_code = 409
                return response
            user.email = email
        if phone_number:
            if (user.phone_number != phone_number) and (
                    User.objects.filter(phone_number__iexact=phone_number).exists()):
                response = JsonResponse(
                    data={
                        'error': 'Email is already connected to another account'
                    }
                )
                response.status_code = 409
                return response
            user.phone_number = phone_number
        if bio:
            user.bio = bio

        user.save()

        return JsonResponse(
            data={
                'success': True,
                'message': 'Profile updated successfully'
            }
        )
    else:
        data = {
            'logged_user': request.user.get_context(),
            'settings': True,
            'profile_settings': True,
            'selector': True
        }
        return render(
            request=request,
            template_name='settings-base.html',
            context=data
        )


@login_required(login_url='user-login')
def settings_change_password(request: HttpRequest):
    if request.method == 'POST':
        try:
            old_password = request.POST['old-password']
            new_password = request.POST['new-password']
        except KeyError:
            response = JsonResponse(
                data={
                    'error': 'Invalid data'
                }
            )
            response.status_code = 400
            return response

        user = User.objects.get(username=request.user.username)
        if not user.check_password(old_password):
            response = JsonResponse(
                data={
                    'error': 'Old password is incorrect'
                }
            )
            response.status_code = 403
            return response

        user.set_password(new_password)
        user.save()

        return JsonResponse(
            data={
                'success': True,
                'message': 'Password updated successfully'
            }
        )
    else:
        data = {
            'logged_user': request.user,
            'settings': True,
            'update_password': True,
            'selector': True
        }
        return render(
            request=request,
            template_name='settings-base.html',
            context=data
        )


@login_required(login_url='user-login')
def settings_delete_account(request: HttpRequest):
    if request.method == 'POST':
        try:
            password = request.POST['password']
        except KeyError:
            response = JsonResponse(
                data={
                    'error': 'Invalid data'
                }
            )
            response.status_code = 400
            return response

        user = User.objects.get(username=request.user.username)
        if not user.check_password(password):
            response = JsonResponse(
                data={
                    'error': 'Password is incorrect'
                }
            )
            response.status_code = 403
            return response

        logout(request)
        user.delete()

        return JsonResponse(
            data={
                'success': True,
                'message': 'Account deleted successfully'
            }
        )
    else:
        data = {
            'logged_user': request.user,
            'settings': True,
            'delete_account': True,
            'selector': True
        }
        return render(
            request=request,
            template_name='settings-base.html',
            context=data
        )