from Admin.helpers import superuser_login_required
from Comments.models import Comment
from Posts.models import Post
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render, get_object_or_404


@superuser_login_required(login_url='admin-login')
def admin_post_page(request: HttpRequest, post_id: int):
    post = get_object_or_404(Post.admin_objects, id=post_id)
    context = {
        'post': post.get_context(user=request.user, comments=True, admin_data=True)
    }
    return render(request, 'admin-post-page.html', context=context)


@superuser_login_required(login_url='admin-login')
def admin_post_delete(request: HttpRequest, post_id: int):
    post = get_object_or_404(Post.admin_objects, id=post_id)
    post.delete()
    return JsonResponse(
        data={
            'success': True,
        }
    )


@superuser_login_required(login_url='admin-login')
def admin_comment_delete(request: HttpRequest, comment_id: int):
    comment = get_object_or_404(Comment.admin_objects, id=comment_id)
    comment.delete()
    return JsonResponse(
        data={
            'success': True,
        }
    )