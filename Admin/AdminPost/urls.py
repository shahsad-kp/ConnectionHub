from django.urls import path

from .views import admin_post_page, admin_post_delete, admin_comment_delete

urlpatterns = [
    path('<int:post_id>/', admin_post_page, name='admin-posts-page'),
    path('<int:post_id>/delete/', admin_post_delete, name='admin-posts-delete'),
    path('comment/<int:comment_id>/delete/', admin_comment_delete, name='admin-comments-delete'),
]