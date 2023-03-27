from typing import Dict

from django.db import models

from ConnectionHub.settings import cipher_suite
from Posts.models import Post
from Users.models import User


class CommentsUserManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().exclude(user__is_banned=True)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    created_at = models.DateTimeField(auto_now_add=True)
    encrypted_content = models.BinaryField()

    @property
    def content(self):
        message_bytes = bytes(self.encrypted_content)
        return cipher_suite.decrypt(message_bytes).decode()

    @content.setter
    def content(self, value):
        self.encrypted_content = cipher_suite.encrypt(value.encode())

    objects = CommentsUserManager()
    admin_objects = models.Manager()

    def __str__(self):
        return f'{self.user} -> {self.post}'

    def get_context(self, **kwargs) -> Dict[str, str]:
        return {
            'id': self.id,
            'user': self.user.get_context(
                **kwargs
            ),
            'content': self.content,
        }
