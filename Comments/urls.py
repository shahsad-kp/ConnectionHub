from django.urls import path

from Comments.views import comments

urlpatterns = [
    path('', comments, name='comments-view')
]
