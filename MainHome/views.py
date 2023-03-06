

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpRequest
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone

from MainHome.models import OtpVerification
from MainUsers.models import User
from utils.posts import get_suggested_posts
from utils.users import get_suggestion_users_context, get_following_users_context


@login_required(login_url='user-login')
def home_view(request):
    user = User.objects.get(username=request.user.username)
    user_suggestions = get_suggestion_users_context(user)
    followings = get_following_users_context(user)
    suggested_posts = get_suggested_posts(user)
    suggested_posts = [
        post.get_context(user)
        for post in suggested_posts
    ]

    context = {
        'suggestions': user_suggestions,
        'followings': followings,
        'post_updates': suggested_posts,
        'logged_user': request.user.get_context()
    }
    return render(
        request=request,
        template_name='user-home.html',
        context=context,
    )


def login_view(request):
    if request.user.is_authenticated:
        return redirect('user-home')
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

        username = username.lower()

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse(
                data={
                    'success': 'Logged in successfully',
                    'redirect': reverse('user-home')
                }
            )
        else:
            response = JsonResponse(
                data={
                    'error': 'Username and password do not match'
                }
            )
            response.status_code = 400
            return response
    return render(
        request=request,
        template_name='user-login.html'
    )


def register_view(request):
    if request.user.is_authenticated:
        return redirect('user-home')
    if request.method == 'POST':
        try:
            username = request.POST['username']
            password = request.POST['password']
            email = request.POST['email']
            fullname = request.POST['fullname']
        except KeyError:
            response = JsonResponse(
                data={
                    'success': False,
                    'error': 'Invalid data'
                }
            )
            response.status_code = 400
            return response
        username = username.lower()
        email = email.lower()
        if User.objects.filter(username=username).exists():
            response = JsonResponse(
                data={
                    'success': False,
                    'error': 'Username already taken'
                }
            )
            response.status_code = 400
            return response

        if User.objects.filter(email=email).exists():
            response = JsonResponse(
                data={
                    'success': False,
                    'error': 'Email already connected to an account'
                }
            )
            response.status_code = 400
            return response

        email_verification = OtpVerification.objects.filter(
            username=username,
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
        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
            full_name=fullname,
            email_verified=True
        )
        user.save()
        user = authenticate(request, username=username, password=password)
        login(request, user)
        return JsonResponse(
            data={
                'success': True,
                'redirect': reverse('user-home')
            }
        )

    return render(
        request,
        template_name='user-register.html'
    )


def logout_view(request):
    logout(request)
    return redirect('user-login')


def send_otp(request: HttpRequest):
    if request.method == 'POST':
        email: str = request.POST.get('email')
        username: str = request.POST.get('username')
        email = email.lower()
        username = username.lower()
        email_verification = OtpVerification(username=username, email=email, type='email')
        email_verification.generate_otp()
        email_verification.send_otp()
        email_verification.save()
        return JsonResponse(
            {
                'status': True,
                'message': 'OTP sent successfully'
            }
        )
    else:
        response = JsonResponse(
            {
                'status': False,
                'error': 'Invalid request'
            }
        )
        response.status_code = 400
        return response


def verify_otp(request):
    if request.method == 'POST':
        otp: str = request.POST.get('otp')
        email: str = request.POST.get('email')
        email = email.lower()
        otp = otp.lower()
        email_verification = OtpVerification.objects.filter(
            email=email,
            otp=otp
        ).first()
        if email_verification and email_verification.verify_otp():
            return JsonResponse({'success': True})
        else:
            response = JsonResponse(
                {
                    'success': False,
                    'error': 'OTP is invalid or expired'
                }
            )
            response.status_code = 400
            return response
    else:
        response = JsonResponse(
            {
                'success': False,
                'error': 'Invalid request'
            }
        )
        response.status_code = 400
        return response


def check_username_availability(request: HttpRequest):
    if not ((request.method == 'GET') & ('q' in request.GET)):
        response = JsonResponse(
            data={
                'error': 'Invalid parameter'
            }
        )
        response.status_code = 400
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
        response.status_code = 400
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
