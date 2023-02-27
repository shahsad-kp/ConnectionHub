from django.urls import path

from .views import post_detail_page, like_post, dislike_post, save_post, add_comment, saved_posts, new_post, \
    view_comments

urlpatterns = [
    path('<int:post_id>/', post_detail_page, name='post-detail'),
    path('<int:post_id>/like/', like_post, name='like-post'),
    path('<int:post_id>/dislike/', dislike_post, name='dislike-post'),
    path('<int:post_id>/save/', save_post, name='save-post'),
    path('<int:post_id>/comment/', view_comments, name='view-comment'),
    path('<int:post_id>/comment/add/', add_comment, name='add-comment'),
    path('saved/', saved_posts, name='saved-posts-dashboards'),
    path('posts/new/', new_post, name='new-post')
]
