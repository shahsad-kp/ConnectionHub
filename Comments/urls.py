from django.urls import path

from Comments.views import comments

urlpatterns = [
    path('<int:post_id>/', comments, name='comments-view')
]
