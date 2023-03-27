from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, JsonResponse, Http404, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from Auth.models import OtpVerification
from .models import User, Follow, Blocks, FollowRequest


@login_required(login_url='user-login')
def home_view(request: HttpRequest, username: str):
    logined_user = User.objects.get(pk=request.user.pk)
    user = get_object_or_404(User.not_blocked_users(logined_user), username=username)
    if user.blocked_users.filter(user=logined_user).exists():
        raise Http404(
            "No %s matches the given query."
        )

    followings = [
        user.get_context(logined_user)
        for user in logined_user.get_all_followings()
    ]
    extra_followings = len(followings[10:])
    followings = followings[:10]

    suggestions = [
        user.get_context(logined_user)
        for user in logined_user.get_suggestions()
    ]

    context = {
        'user': user.get_context(
            logined_user=logined_user,
            posts=True,
        ),
        'suggestions': suggestions,
        'followings': followings,
        'extra_followings': extra_followings,
        'logged_user': request.user.get_context(),
        'self_profile_tab': request.user == user,
        'new_messages': logined_user.get_new_messages().exists(),
        'new_notifications': request.user.get_new_notifications().count()
    }

    if (
            user.settings.private_account and
            not user.followers.filter(follower=logined_user).exists()
    ) and logined_user != user:
        context['requested'] = FollowRequest.objects.filter(
            follower=logined_user,
            followee=user,
        ).exists()
        return render(
            request=request,
            template_name='private-account.html',
            context=context
        )
    else:
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
    user = User.objects.get(pk=request.user.pk)
    query = request.GET['q']
    results = user.search_users(query)
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
    org_user = User.objects.get(username=request.user.username)
    user = get_object_or_404(User.not_blocked_users(org_user), username=username)
    if Follow.objects.filter(follower=org_user, followee=user).exists():
        response = JsonResponse(
            {
                'success': False,
                'error': 'Already followed'
            }
        )
        user.save()
        response.status_code = 400
    elif user.settings.private_account:
        response = JsonResponse(
            {
                'success': False,
                'error': 'User has private account'
            }
        )
        response.status_code = 400
    else:
        org_user.follow(user)
        response = JsonResponse(
            {
                'success': True,
                'followed': True,
                'private_account': user.settings.private_account,
                'followers': user.followers_count,
                'followings': user.followings_count,
            }
        )
    return response


@login_required(login_url='user-login')
def unfollow_user(request: HttpRequest, username: str):
    org_user = User.objects.get(username=request.user.username)
    user: User = get_object_or_404(User.not_blocked_users(org_user), username=username)
    if Follow.objects.filter(follower=org_user, followee=user).exists():
        org_user.unfollow(user)
        user.refresh_from_db(
            fields=[
                'followers_count',
                'followings_count'
            ]
        )
        response = JsonResponse(
            {
                'success': True,
                'followed': False,
                'private_account': user.settings.private_account,
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
def send_follow_request(request: HttpRequest, username: str):
    logined_user = User.objects.get(username=request.user.username)
    user = get_object_or_404(User.not_blocked_users(logined_user), username=username)
    if not user.settings.private_account:
        response = JsonResponse(
            {
                'success': False,
                'requested': False,
                'error': 'User has public account'
            }
        )
        response.status_code = 400
    elif Follow.objects.filter(follower=logined_user, followee=user).exists():
        response = JsonResponse(
            {
                'success': False,
                'requested': False,
                'error': 'Already followed'
            }
        )
        response.status_code = 400
    elif FollowRequest.objects.filter(follower=logined_user, followee=user).exists():
        response = JsonResponse(
            {
                'success': False,
                'requested': True,
                'error': 'Already requested'
            }
        )
        response.status_code = 400
    else:
        FollowRequest.objects.create(
            follower=logined_user,
            followee=user,
        )
        response = JsonResponse(
            {
                'success': True,
                'requested': True,
            }
        )
    return response


@login_required(login_url='user-login')
def cancel_follow_request(request: HttpRequest, username: str):
    logined_user = User.objects.get(username=request.user.username)
    user = get_object_or_404(User.not_blocked_users(logined_user), username=username)
    if FollowRequest.objects.filter(follower=logined_user, followee=user).exists():
        FollowRequest.objects.filter(follower=logined_user, followee=user).delete()
        response = JsonResponse(
            {
                'success': True,
                'requested': False,
            }
        )
    else:
        response = JsonResponse(
            {
                'success': False,
                'requested': False,
                'error': 'Not requested'
            }
        )
        response.status_code = 400

    return response


@login_required(login_url='user-login')
def respond_follow_request(request: HttpRequest, username: str, action: str):
    logined_user = User.objects.get(username=request.user.username)
    user = get_object_or_404(User.not_blocked_users(logined_user), username=username)
    if not logined_user.settings.private_account:
        response = JsonResponse(
            {
                'success': False,
                'followed': False,
                'error': 'User has public account'
            }
        )
        response.status_code = 400
    elif not FollowRequest.objects.filter(follower=user, followee=logined_user).exists():
        response = JsonResponse(
            {
                'success': False,
                'followed': False,
                'error': 'Not requested'
            }
        )
        response.status_code = 400
    elif action == 'accept':
        response = _accept_follow_request(request=request, user=user, logined_user=logined_user)

    elif action == 'reject':
        response = _reject_follow_request(request=request, user=user, logined_user=logined_user)
    else:
        response = JsonResponse(
            {
                'success': False,
                'followed': False,
                'error': 'Invalid action'
            }
        )
        response.status_code = 400

    return response


def _accept_follow_request(request: HttpRequest, user: 'User', logined_user: 'User') -> HttpResponse:
    if Follow.objects.filter(follower=user, followee=logined_user).exists():
        response = JsonResponse(
            {
                'success': False,
                'error': 'Already followed'
            }
        )
        response.status_code = 400

    else:
        request = FollowRequest.objects.filter(follower=user, followee=logined_user).first()
        request.accept()
        response = JsonResponse(
            {
                'success': True,
                'followed': True,
                'followers': user.followers_count,
                'followings': user.followings_count,
            }
        )
    return response


def _reject_follow_request(request: HttpRequest, user: 'User', logined_user: 'User'):
    request = FollowRequest.objects.filter(follower=user, followee=logined_user).first()
    request.decline()
    response = JsonResponse(
        {
            'success': True,
            'followed': False,
            'followers': user.followers_count,
            'followings': user.followings_count,
        }
    )

    return response


@login_required(login_url='user-login')
def block_user(request: HttpRequest, username: str):
    org_user = User.objects.get(username=request.user.username)
    user = get_object_or_404(User.not_blocked_users(org_user), username=username)
    if Blocks.objects.filter(user=user, blocked_by=org_user).exists():
        return JsonResponse(
            data={
                'success': False,
                'error': 'Already blocked'
            },
            status=400
        )
    else:
        org_user.block(user)
        return JsonResponse(
            {
                'success': True,
                'blocked': True,
            }
        )


@login_required(login_url='user-login')
def unblock_user(request: HttpRequest, username: str):
    org_user = User.objects.get(username=request.user.username)
    user = get_object_or_404(User.not_blocked_users(org_user), username=username)
    if not Blocks.objects.filter(user=user, blocked_by=org_user).exists():
        return JsonResponse(
            data={
                'success': False,
                'error': 'This user was not blocked'
            },
            status=400
        )
    else:
        org_user.unblock(user)
        return JsonResponse(
            data={
                'success': True,
                'blocked': False
            }
        )


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
            email_otp = request.POST.get('email-otp')
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

            if not email_otp:
                return JsonResponse(
                    data={
                        'success': False,
                        'error': 'Email not verified'
                    },
                    status=400
                )
            email_verification = OtpVerification.objects.filter(
                email=email,
                otp__exact=email_otp
            ).first()
            if email_verification and not email_verification.verified:
                response = JsonResponse(
                    data={
                        'success': False,
                        'error': 'Email is not verified'
                    }
                )
                response.status_code = 400
                return response
            elif email_verification and email_verification.verified:
                email_verification.delete()
            else:
                response = JsonResponse(
                    data={
                        'success': False,
                        'error': 'Email is not verified'
                    }
                )
                response.status_code = 400
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
            'logged_user': request.user.get_context(full_data=True),
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
            'selector': True,
            'new_notifications': request.user.get_new_notifications().count()
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
            'selector': True,
            'new_notifications': request.user.get_new_notifications().count()
        }
        return render(
            request=request,
            template_name='settings-base.html',
            context=data
        )
