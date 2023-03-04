import os
import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Q


def generate_filename(instance: 'User', filename):
    """Generates a filename for the uploaded image based on the user's username and a random UUID."""
    ext = os.path.splitext(filename)[1]
    user_id = instance.id
    random_id = str(uuid.uuid4())
    return f"profile_pictures/{user_id}/{random_id}{ext}"


class User(AbstractUser):
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255, blank=True)
    profile_picture = models.ImageField(
        upload_to=generate_filename,
        default='/profile_pictures/avatar-alt.svg'
    )
    bio = models.TextField(blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    email_verified = models.BooleanField(default=False)
    followers_count = models.IntegerField(default=0)
    followings_count = models.IntegerField(default=0)

    def __str__(self):
        return self.username

    def follow(self, user: 'User'):
        user.followers_count += 1
        self.followings_count += 1
        user.save()
        self.save()
        Follow.objects.create(follower=self, followee=user).save()

    def unfollow(self, user: 'User'):
        user.followers_count -= 1
        self.followings_count -= 1
        user.save()
        self.save()
        Follow.objects.filter(follower=self, followee=user).delete()

    def get_all_followings(self):
        list_of_followings = [following.followee for following in self.followings.all()]
        return list_of_followings

    def get_all_followers(self):
        list_of_followers = [follower.follower for follower in self.followers.all()]
        return list_of_followers

    def get_suggestions(self):
        followed_user_ids = self.followers.all().values_list('id', flat=True)
        users_not_followed = User.objects.exclude(Q(id=self.id) | Q(id__in=followed_user_ids))
        return users_not_followed

    def get_posts(self):
        return self.posts.all().order_by('-created_at')

    def get_context(
            self,
            logined_user: 'User' = None,
            posts: bool = False,
    ):
        if not logined_user:
            logined_user = self

        if posts:
            posts = [post.get_context(logined_user) for post in self.get_posts()]
        else:
            posts = []

        return {
            'username': self.username,
            'fullname': self.full_name,
            'profile_picture': self.profile_picture.url,
            'bio': self.bio,
            'posts': posts,
            'number_of_followers': self.followers_count,
            'number_of_followings': self.followings_count,
            'is_following': Follow.objects.filter(follower=logined_user, followee=self).exists(),
            'self': logined_user.id == self.id,
        }

    def get_suggestion_user_context(self):
        return


class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followings')
    followee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')

    def __str__(self):
        return f'{self.followee} follows {self.follower}'
