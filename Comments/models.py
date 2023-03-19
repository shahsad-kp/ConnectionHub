from typing import Dict

from django.db import models

from Posts.models import Post
from Users.models import User


class CommentsUserManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().exclude(user__is_banned=True)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    objects = CommentsUserManager()
    admin_objects = models.Manager()

    def __str__(self):
        return self.content

    def get_context(self, **kwargs) -> Dict[str, str]:
        return {
            'id': self.id,
            'user': self.user.get_context(
                **kwargs
            ),
            'content': self.content,
        }
