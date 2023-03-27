import os
import uuid
from typing import Dict

from django.db import models
from django.db.models import Q
from django.urls import reverse

from Users.models import User


def generate_filename(instance: 'Post', filename):
    """Generates a filename for the uploaded image based on the user's username and a random UUID."""
    ext = os.path.splitext(filename)[1]
    user_id = instance.user.id
    random_id = str(uuid.uuid4())
    return f"posts/{user_id}/{random_id}{ext}"


class PostsUserManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().exclude(user__is_banned=True)


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    image = models.ImageField(upload_to=generate_filename)
    caption = models.CharField(max_length=255, blank=True)
    location = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    likes_count = models.IntegerField(default=0)
    dislikes_count = models.IntegerField(default=0)
    comments_count = models.IntegerField(default=0)

    objects = PostsUserManager()
    admin_objects = models.Manager()

    def __str__(self):
        return f"Post {self.id} of {self.user}"

    @classmethod
    def not_blocked_posts(cls, logined_user: 'User'):
        return cls.objects.exclude(Q(user__blocked_users__user=logined_user) & ~Q(user=logined_user))

    def get_context(self, user: 'User', comments: bool = False, admin_data: bool = False) -> Dict[str, str]:
        if admin_data:
            from Comments.models import Comment
            comments = [
                comment.get_context()
                for comment in Comment.admin_objects.filter(post=self).order_by('-created_at')
            ]
        if comments:
            comments = [
                comment.get_context(logined_user=user)
                for comment in self.comments.all().order_by('-created_at')
            ]
        else:
            comments = []

        return {
            'id': self.id,
            'user': self.user.get_context(
                logined_user=user if not admin_data else None,
                full_data=True
            ),
            'image': self.image.url,
            'caption': self.caption,
            'location': self.location,
            'likes': self.likes_count,
            'dislikes': self.dislikes_count,
            'liked': self.reactions.filter(user=user, reaction='like').exists(),
            'disliked': self.reactions.filter(user=user, reaction='dislike').exists(),
            'comments_count': self.comments_count,
            'comments': comments,
            'saved': self.saved_by.filter(user=user).exists(),
            'url': reverse(
                'post-detail',
                kwargs={
                    'post_id': self.id
                }
            ),
            'tags': [
                tag.name.replace('#', '')
                for tag in self.tags.all()
            ],
        }


class Reaction(models.Model):
    REACTION_TYPES = [
        ('like', 'Like'),
        ('dislike', 'Dislike'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reactions')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='reactions')
    reaction = models.CharField(choices=REACTION_TYPES, max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._old_reaction = self.reaction

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self._old_reaction = self.reaction

    def __str__(self):
        return self.reaction

    def __repr__(self):
        return f'<Reaction {self.id}>'

    @property
    def old_reaction(self):
        return self._old_reaction


class Tag(models.Model):
    name = models.CharField(max_length=255)
    posts = models.ManyToManyField(Post, related_name='tags')

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'<Tag {self.id}>'


class SavedPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_posts')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='saved_by')
    saved_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} saved {self.post}"
