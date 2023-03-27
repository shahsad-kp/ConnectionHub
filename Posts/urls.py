from django.urls import path

from .views import *

urlpatterns = [
    path('saved/', saved_posts, name='saved-posts-dashboards'),
    path('new/', new_post, name='new-post'),
    path('<int:post_id>/', post_detail_page, name='post-detail'),
    path('<int:post_id>/like/', like_post, name='like-post'),
    path('<int:post_id>/dislike/', dislike_post, name='dislike-post'),
    path('<int:post_id>/save/', save_post, name='save-post'),
    path('<int:post_id>/delete/', delete_post, name='delete-post'),
    path('tag/<str:tag_name>/', tag_posts, name='tag-posts'),
]
