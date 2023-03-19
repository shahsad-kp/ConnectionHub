from django.urls import path

from Comments.views import comments, delete_comment

urlpatterns = [
    path('<int:post_id>/', comments, name='comments-view'),
    path('<int:comment_id>/delete/', delete_comment, name='delete-comment')
]
