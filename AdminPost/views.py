from django.http import HttpRequest, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from MainPosts.models import Post, Comment
from utils.helpers import superuser_login_required


@superuser_login_required(login_url='admin-login')
def admin_post_page(request: HttpRequest, post_id: int):
    post = get_object_or_404(Post, id=post_id)
    context = {
        'post': post.image.url,
        'likes': post.likes.count(),
        'dislikes': post.dislikes.count(),
        'comments': [
            {
                'user': comment.user.username,
                'content': comment.content,
                'delete_url': reverse(
                    viewname='admin-comments-delete',
                    args=[
                        comment.id
                    ]
                )
            }
            for comment in post.comments.all()
        ],
        'tags': [
            tag.name
            for tag in post.tags.all()
        ],
    }
    return render(request, 'admin_post_page.html', context=context)


@superuser_login_required(login_url='admin-login')
def admin_post_delete(request: HttpRequest, post_id: int):
    post = get_object_or_404(Post, id=post_id)
    post.delete()
    return JsonResponse(
        data={
            'success': True,
        }
    )


@superuser_login_required(login_url='admin-login')
def admin_comment_delete(request: HttpRequest, comment_id: int):
    comment = get_object_or_404(Comment, id=comment_id)
    comment.delete()
    return JsonResponse(
        data={
            'success': True,
        }
    )
