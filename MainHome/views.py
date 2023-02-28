from datetime import datetime

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpRequest
from django.shortcuts import redirect, render

from MainHome.models import EmailVerification
from MainUsers.models import User


@login_required(login_url='user-login')
def home_view(request):
    suggestions = request.user.get_suggestions()
    followings = request.user.get_all_followings()
    suggested_posts = []
    for user in followings:
        suggested_posts.extend(
            user.get_posts()
        )
    suggested_posts.sort(
        key=lambda x: x.created_at,
        reverse=True
    )
    context = {
        'suggestions': suggestions,
        'followings': followings,
        'suggest_posts': suggested_posts,
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
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('user-home')
        else:
            response = JsonResponse(
                data={
                    'error': 'Invalid username or password'
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
                    'error': 'Invalid data'
                }
            )
            response.status_code = 400
            return response

        if User.objects.filter(username=username).exists():
            response = JsonResponse(
                data={
                    'error': 'Username already taken'
                }
            )
            response.status_code = 400
            return response

        if User.objects.filter(email=email).exists():
            response = JsonResponse(
                data={
                    'error': 'Email already connected to an account'
                }
            )
            response.status_code = 400
            return response

        email_verification = EmailVerification.objects.filter(
            username=username,
            expires_at__gt=datetime.now(),
        ).first()
        if email_verification and not email_verification.verified:
            response = JsonResponse(
                data={
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
                    'error': 'Email is not verified'
                }
            )
            response.status_code = 400
            return response
        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
            full_name=fullname
        )
        user.save()
        send_otp(email, user)
        return render(
            request,
            template_name='user-home.html',
            context={'email': email}
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
        email = request.POST.get('email')
        username = request.POST.get('username')
        email_verification = EmailVerification(username=username, email=email)
        email_verification.generate_otp()
        email_verification.send_otp()
        email_verification.save()


def verify_otp(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        email = request.POST.get('email')
        email_verification = EmailVerification.objects.filter(
            email=email,
            otp=otp,
            expires_at__gt=datetime.now(),
        ).first()
        if email_verification:
            email_verification.verified = True
            email_verification.save()
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error'})
    else:
        return JsonResponse({'status': 'error'})
