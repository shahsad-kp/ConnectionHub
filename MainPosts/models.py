import os
import uuid

from django.db import models

from MainUsers.models import User


def generate_filename(instance: 'Post', filename):
    """Generates a filename for the uploaded image based on the user's username and a random UUID."""
    ext = os.path.splitext(filename)[1]
    user_id = instance.user.id
    random_id = str(uuid.uuid4())
    return f"posts/{user_id}/{random_id}{ext}"


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    image = models.ImageField(upload_to=generate_filename)
    caption = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Post {self.id} of {self.user}"

    def __repr__(self):
        return f'<Post {self.id}>'

    @property
    def likes(self):
        return self.reactions.filter(reaction='like')

    @property
    def dislikes(self):
        return self.reactions.filter(reaction='dislike')


class Reaction(models.Model):
    REACTION_TYPES = [
        ('like', 'Like'),
        ('dislike', 'Dislike'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='reactions')
    reaction = models.CharField(choices=REACTION_TYPES, max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.reaction

    def __repr__(self):
        return f'<Reaction {self.id}>'


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content

    def __repr__(self):
        return f'<Comment {self.id}>'


class Tag(models.Model):
    name = models.CharField(max_length=255)
    post = models.ManyToManyField(Post, related_name='tags')

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'<Tag {self.id}>'


class SavedPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_posts')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='saved_by')

    def __str__(self):
        return f"{self.user} saved {self.post}"
