from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render, redirect

from MainUsers.models import User


@login_required(login_url='user-login')
def settings_home(request: HttpRequest):
    return redirect('profile-settings')


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
                'success': True
            }
        )
    else:
        return render(
            request=request,
            template_name='profile-update-settings.html'
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
                'success': True
            }
        )
    else:
        return render(
            request=request,
            template_name='profile-change-password.html'
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

        user.delete()

        return JsonResponse(
            data={
                'success': True
            }
        )
    else:
        return render(
            request=request,
            template_name='profile-delete-account.html'
        )


@login_required(login_url='user-login')
def help_view(request: HttpRequest):
    if request.method == 'POST':
        try:
            subject = request.POST['subject']
            message = request.POST['message']
        except KeyError:
            response = JsonResponse(
                data={
                    'error': 'Invalid data'
                }
            )
            response.status_code = 400
            return response

        user = User.objects.get(username=request.user.username)
        user.help_messages.create(
            subject=subject,
            message=message
        )
        return JsonResponse(
            data={
                'success': True
            }
        )
    return render(
        request=request,
        template_name='help-center.html'
    )
