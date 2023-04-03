from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from utils.posts import get_saved_posts_context
from .models import Post, Reaction, Tag


@login_required(login_url='user-login')
def post_detail_page(request: HttpRequest, post_id: int):
    logined_user = request.user
    post = get_object_or_404(Post.not_blocked_posts(logined_user), id=post_id)
    if (
            post.user.settings.private_account and
            not post.user.followers.filter(follower=logined_user).exists()
    ) and not logined_user == post.user:
        return redirect(
            reverse(
                'profile-pages',
                kwargs={
                    'username': post.user.username
                }
            )
        )

    context = {
        'post': post.get_context(logined_user, True),
        'logged_user': request.user.get_context(),
        'new_notifications': request.user.get_new_notifications().count()
    }
    return render(request, 'post-detail.html', context=context)


@login_required(login_url='user-login')
def like_post(request: HttpRequest, post_id: int):
    post: Post = get_object_or_404(Post.not_blocked_posts(request.user), id=post_id)
    user = request.user
    reaction = post.reactions.filter(user=user).first()
    if not reaction:
        Reaction.objects.create(user=request.user, post=post, reaction='like')
        liked = True
        disliked = False
    elif reaction.reaction == 'like':
        reaction.delete()
        liked = False
        disliked = False
    else:
        reaction.reaction = 'like'
        reaction.save()
        liked = True
        disliked = False

    post.refresh_from_db()
    return JsonResponse(
        data={
            'success': True,
            'likes': post.likes_count,
            'dislikes': post.dislikes_count,
            'liked': liked,
            'disliked': disliked
        }
    )


@login_required(login_url='user-login')
def dislike_post(request: HttpRequest, post_id: int):
    post: Post = get_object_or_404(Post.not_blocked_posts(request.user), id=post_id)
    user = request.user
    reaction = post.reactions.filter(user=user).first()
    if not reaction:
        Reaction.objects.create(user=request.user, post=post, reaction='dislike')
        disliked = True
        liked = False
    elif reaction.reaction == 'dislike':
        reaction.delete()
        liked = False
        disliked = False
    else:
        reaction.reaction = 'dislike'
        reaction.save()
        disliked = True
        liked = False

    post.refresh_from_db()
    return JsonResponse(
        data={
            'success': True,
            'likes': post.likes_count,
            'dislikes': post.dislikes_count,
            'liked': liked,
            'disliked': disliked
        }
    )


@login_required(login_url='user-login')
def save_post(request: HttpRequest, post_id: int):
    post = get_object_or_404(Post.not_blocked_posts(request.user), id=post_id)
    if post.saved_by.filter(user=request.user).exists():
        post.saved_by.filter(user=request.user).delete()
        saved = False
    else:
        post.saved_by.create(user=request.user)
        saved = True
    return JsonResponse(
        data={
            'success': True,
            'saved': saved
        }
    )


@login_required(login_url='user-login')
def saved_posts(request: HttpRequest):
    new_messages = request.user.get_new_messages()
    data = {
        'saved_posts_rows': get_saved_posts_context(request.user),
        'logged_user': request.user.get_context(),
        'saved_posts_tab': True,
        'new_messages': new_messages.exists(),
        'new_notifications': request.user.get_new_notifications().count()
    }
    data['number_of_saved_posts'] = len(data['saved_posts_rows'][0]) + len(data['saved_posts_rows'][1])
    return render(request, 'saved-posts-dashboard.html', context=data)


@login_required(login_url='user-login')
def tag_posts(request: HttpRequest, tag_name: str):
    tag = Tag.objects.filter(name='#' + tag_name).first()
    if not tag:
        posts = []
    else:
        posts = tag.posts.all()
    posts_rows = [[], []]
    for index, post in enumerate(
            iterable=posts,
            start=0
    ):
        posts_rows[index % 2].append(post.get_context(request.user))
    new_messages = request.user.get_new_messages()
    data = {
        'logged_user': request.user.get_context(),
        'posts_rows': posts_rows,
        'new_messages': new_messages.exists(),
        'new_notifications': request.user.get_new_notifications().count(),
        'tag': tag_name
    }
    data['number_of_posts'] = len(data['posts_rows'][0]) + len(data['posts_rows'][1])
    return render(request, 'tag-dashboard.html', context=data)


@login_required(login_url='user-login')
def new_post(request: HttpRequest):
    if request.method == 'POST':
        try:
            image = request.FILES['image']
            caption = request.POST['caption']
            tags = request.POST['tags']
            location = request.POST['location']
        except KeyError:
            response = JsonResponse(
                data={
                    'error': 'Invalid data',
                }
            )
            response.status_code = 400
            return response
        post = Post.objects.create(
            user=request.user,
            image=image,
            caption=caption,
            location=location
        )
        for tag_name in str(tags).strip().split(' '):
            tag_name = tag_name.strip()
            if not tag_name:
                continue
            tag, _ = Tag.objects.get_or_create(name=tag_name)
            post.tags.add(tag)

        return JsonResponse(
            data={
                'success': 'Logged in successfully',
                'redirect': reverse('post-detail', args=[post.id])
            }
        )
    else:
        return render(
            request,
            'new-post.html',
            context={
                'logged_user': request.user.get_context(),
                'new_post_tab': True,
                'new_notifications': request.user.get_new_notifications().count()
            }
        )


@login_required(login_url='user-login')
def delete_post(request: HttpRequest, post_id):
    post = get_object_or_404(Post, id=post_id)
    if not post.user == request.user:
        return JsonResponse(
            data={
                'success': False,
                'error': 'You are not allowed to do this'
            },
            status=403
        )

    post.delete()
    return JsonResponse(
        data={
            'success': True,
            'redirect_url': reverse(
                viewname='profile-pages',
                kwargs={
                    'username': post.user.username
                }
            )
        }
    )
