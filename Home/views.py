from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from Users.models import User
from utils.posts import get_suggested_post


@login_required(login_url='user-login')
def home_view(request: HttpRequest) -> HttpResponse:
    user = User.objects.get(username=request.user.username)
    user_suggestions = [
        suggestion_user.get_context(user)
        for suggestion_user in user.get_suggestions()
    ]
    followings = [
        following_user.get_context(user)
        for following_user in user.get_all_followings()
    ]
    suggested_posts = get_suggested_post(user)
    suggested_posts = [
        post.get_context(user)
        for post in suggested_posts
    ]
    new_messages = user.get_new_messages()
    extra_followings = len(followings[10:])
    followings = followings[:10]

    context = {
        'suggestions': user_suggestions,
        'followings': followings,
        'extra_followings': extra_followings,
        'post_updates': suggested_posts,
        'logged_user': request.user.get_context(),
        'home_tab': True,
        'new_messages': new_messages.exists(),
        'new_notifications': request.user.get_new_notifications().count()
    }
    return render(
        request=request,
        template_name='users-home-page.html',
        context=context,
    )


@login_required(login_url='user-login')
def settings_home(request: HttpRequest) -> HttpResponse:
    context = {
        'logged_user': request.user.get_context(),
        'profile_settings': False,
        'update_password': False,
        'delete_account': False,
        'help_center': False,
        'settings': True,
        'new_notifications': request.user.get_new_notifications().count()
    }
    return render(
        request=request,
        template_name='settings-base.html',
        context=context,
    )
