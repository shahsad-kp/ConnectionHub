from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from utils.posts import get_saved_posts_context
from .models import Post, Reaction, Tag


@login_required(login_url='user-login')
def post_detail_page(request: HttpRequest, post_id: int):
    post = get_object_or_404(Post, id=post_id)
    user = request.user
    context = {
        'post': post.get_context(user, True),
        'logged_user': request.user.get_context()
    }
    return render(request, 'post-detail.html', context=context)


@login_required(login_url='user-login')
def like_post(request: HttpRequest, post_id: int):
    post = get_object_or_404(Post, id=post_id)
    like = post.likes.filter(user=request.user)
    dislike = post.dislikes.filter(user=request.user)
    if like.exists():
        like.delete()
        liked = False
        disliked = False
    elif dislike.exists():
        dislike.delete()
        Reaction.objects.create(user=request.user, post=post, reaction='like')
        liked = True
        disliked = False
    else:
        Reaction.objects.create(user=request.user, post=post, reaction='like')
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
    post = get_object_or_404(Post, id=post_id)
    like = Reaction.objects.filter(user=request.user, post=post, reaction='like')
    dislike = Reaction.objects.filter(user=request.user, post=post, reaction='dislike')
    if dislike.exists():
        dislike.delete()
        liked = False
        disliked = False
    elif like.exists():
        like.delete()
        Reaction.objects.create(user=request.user, post=post, reaction='dislike')
        disliked = True
        liked = False
    else:
        Reaction.objects.create(user=request.user, post=post, reaction='dislike')
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
    post = get_object_or_404(Post, id=post_id)
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
    data = {
        'saved_posts_rows': get_saved_posts_context(request.user),
        'logged_user': request.user.get_context()
    }
    data['number_of_saved_posts'] = len(data['saved_posts_rows'][0]) + len(data['saved_posts_rows'][1])
    return render(request, 'saved-posts-dashboard.html', context=data)


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
        for tag_name in str(tags).split(','):
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
                'logged_user': request.user.get_context()
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
            'success': True
        }
    )
