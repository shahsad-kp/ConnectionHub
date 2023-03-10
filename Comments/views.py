from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpRequest
from django.shortcuts import get_object_or_404

from Posts.models import Post


@login_required(login_url='user-login')
def comments(request: HttpRequest, post_id: int):
    post = get_object_or_404(Post, id=post_id)
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
        post.comments_count += 1
        post.save()
        return JsonResponse(
            data={
                'success': True,
                'comments': [
                    comment.get_context()
                    for comment in post.comments.all()
                ],
            }
        )
    return JsonResponse(
        data={
            'success': True,
            'comments': [
                comment.get_context()
                for comment in post.comments.all()
            ],
        }
    )
