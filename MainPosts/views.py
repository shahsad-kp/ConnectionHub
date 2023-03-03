from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from MainPosts.models import Post, Reaction, Tag


@login_required(login_url='user-login')
def post_detail_page(request: HttpRequest, post_id: int):
    post = get_object_or_404(Post, id=post_id)
    context = {
        'post': post.image.url,
        'likes': post.likes.count(),
        'dislikes': post.dislikes.count(),
        'comments': [
            {
                'user': {
                    'username': comment.user.username,
                    'profile_picture': comment.user.profile_picture.url if comment.user.profile_picture else '',
                },
                'content': comment.content,
            }
            for comment in post.comments.all()
        ],
        'tags': [
            tag.name
            for tag in post.tags.all()
        ],
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
        post.likes_count -= 1
    elif dislike.exists():
        dislike.delete()
        Reaction.objects.create(user=request.user, post=post, reaction='like')
        liked = True
        disliked = False
        post.likes_count += 1
        post.dislikes_count -= 1
    else:
        Reaction.objects.create(user=request.user, post=post, reaction='like')
        liked = True
        disliked = False
        post.likes_count += 1
    post.save()
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
        post.dislikes_count -= 1
    elif like.exists():
        like.delete()
        Reaction.objects.create(user=request.user, post=post, reaction='dislike')
        disliked = True
        liked = False
        post.dislikes_count += 1
        post.likes_count -= 1
    else:
        Reaction.objects.create(user=request.user, post=post, reaction='dislike')
        disliked = True
        liked = False
        post.dislikes_count += 1
    post.save()
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
def view_comments(request: HttpRequest, post_id: int):
    post = get_object_or_404(Post, id=post_id)
    return JsonResponse(
        data={
            'success': True,
            'comments': [
                {
                    'user': {
                        'username': comment.user.username,
                        'profile_picture': comment.user.profile_picture.url if comment.user.profile_picture else '',
                        'url': reverse('profile-pages', args=[comment.user.username])
                    },
                    'content': comment.content,
                }
                for comment in post.comments.all()
            ],
        }
    )


@login_required(login_url='user-login')
def add_comment(request: HttpRequest, post_id: int):
    if request.method == 'POST':
        post = get_object_or_404(Post, id=post_id)
        if ('comment' not in request.POST) or (not bool(request.POST['comment'])):
            response = JsonResponse(
                data={
                    'success': False,
                    'error': 'Comment is required'
                }
            )
            response.status_code = 400
            return response

        comment = request.POST['comment']
        post.comments.create(user=request.user, content=comment)
        return JsonResponse(
            data={
                'success': True,
                'comments': [
                    {
                        'user': {
                            'username': comment.user.username,
                            'profile_picture': comment.user.profile_picture.url if comment.user.profile_picture else '',
                            'url': reverse('profile-pages', args=[comment.user.username])
                        },
                        'content': comment.content,
                    }
                    for comment in post.comments.all()
                ],
            }
        )
    else:
        return redirect('post-detail', post_id=post_id)


@login_required(login_url='user-login')
def saved_posts(request: HttpRequest):
    data = {
        'saved_posts': [
            {
                'image': post.image.url,
                'likes': post.likes.count(),
                'dislikes': post.dislikes.count(),
                'caption': post.caption,
                'url': reverse('post-detail', args=[post.id]),
                'tags': [
                    tag.name
                    for tag in post.tags.all()
                ],
                'user': {
                    'username': post.user.username,
                    'profile_picture': post.user.profile_picture.url if post.user.profile_picture else '',
                    'url': reverse('profile-pages', args=[post.user.username])
                }
            }
            for post in request.user.saved_posts.all()
        ]
    }
    return render(request, 'saved-posts-dashboard.html', context=data)


@login_required(login_url='user-login')
def new_post(request: HttpRequest):
    if request.method == 'POST':
        try:
            image = request.FILES['image']
            caption = request.POST['caption']
            tags = request.POST['tags']
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
            caption=caption
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
        return render(request, 'new-post.html')
