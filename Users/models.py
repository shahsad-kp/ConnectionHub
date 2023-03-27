import os
import uuid

from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.db.models import Q, QuerySet


def generate_filename(instance: 'User', filename):
    """Generates a filename for the uploaded image based on the user's username and a random UUID."""
    ext = os.path.splitext(filename)[1]
    user_id = instance.id
    random_id = str(uuid.uuid4())
    return f"profile_pictures/{user_id}/{random_id}{ext}"


class UsersUserManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().exclude(is_banned=True)


class FollowsUserManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().exclude(followee__is_banned=True).exclude(follower__is_banned=True)


class BlocksUserManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().exclude(user__is_banned=True).exclude(blocked_by__is_banned=True)


class FollowRequestUserManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().exclude(followee__is_banned=True).exclude(follower__is_banned=True)


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
    is_banned = models.BooleanField(default=False)

    objects = UsersUserManager()
    admin_objects = models.Manager()

    def __str__(self):
        return '@' + self.username

    @classmethod
    def not_blocked_users(cls, logined_user: 'User'):
        return cls.objects.exclude(blocked_users__user=logined_user)

    def follow(self, user: 'User'):
        Follow.objects.create(follower=self, followee=user).save()

    def unfollow(self, user: 'User'):
        Follow.objects.filter(follower=self, followee=user).delete()

    def block(self, user: 'User'):
        Follow.objects.filter(Q(follower=self, followee=user) | Q(follower=user, followee=self)).delete()
        Blocks.objects.create(user=user, blocked_by=self).save()

    def unblock(self, user: 'User'):
        Blocks.objects.filter(user=user, blocked_by=self).delete()

    def get_all_followings(self):
        list_of_followings = [following.followee for following in self.followings.all().order_by('-followed_at')]
        return list_of_followings

    def get_all_followers(self):
        list_of_followers = [follower.follower for follower in self.followers.all()]
        return list_of_followers

    def get_suggestions(self):
        users_not_followed = User.not_blocked_users(self).filter(
            followers__follower__followers__follower=self
        ).exclude(
            Q(username=self.username) |
            Q(followers__follower=self) |
            Q(follow_requests__follower=self)
        ).distinct().order_by('-followers_count')[:10]
        return users_not_followed

    def get_new_messages(self) -> QuerySet:
        return self.receiver_messages.filter(viewed=False)

    def get_new_notifications(self) -> QuerySet:
        return self.notifications.filter(viewed=False)

    def get_posts(self):
        return self.posts.all().order_by('-created_at')

    def get_context(
            self,
            logined_user: 'User' = None,
            full_data: bool = False,
            posts: bool = False,
            admin_data: bool = False,
            extra_data: dict = None
    ):
        if not logined_user:
            logined_user = self

        if admin_data:
            from Posts.models import Post
            posts = [post.get_context(user=logined_user, admin_data=admin_data) for post in
                     Post.admin_objects.filter(user=self).order_by('-created_at')]
        elif posts:
            posts = [post.get_context(user=logined_user, admin_data=admin_data) for post in self.posts.all().order_by('-created_at')]
        else:
            posts = []

        data = {
            'username': self.username,
            'fullname': self.full_name,
            'profile_picture': self.profile_picture.url,
            'bio': self.bio,
            'posts': posts,
            'number_of_followers': self.followers_count,
            'number_of_followings': self.followings_count,
            'is_following': Follow.objects.filter(follower=logined_user, followee=self).exists(),
            'self': logined_user.id == self.id,
            'is_banned': self.is_banned,
            'blocked': self.blockers.filter(blocked_by=logined_user).exists(),
            'private': self.settings.private_account
        }
        if (not (admin_data or full_data)) and self.is_banned:
            data = {
                'username': self.username,
                'fullname': 'Not Available',
                'profile_picture': '/media/profile_pictures/avatar-alt.svg',
                'bio': None,
                'posts': [],
                'number_of_followers': 0,
                'number_of_followings': 0,
                'is_following': Follow.objects.filter(follower=logined_user, followee=self).exists(),
                'self': logined_user.id == self.id,
                'is_banned': self.is_banned,
                'blocked': False
            }
        if admin_data or full_data:
            data['date_joined'] = self.date_joined
            data['last_login'] = self.last_login
            data['phone'] = self.phone_number
            data['email'] = self.email
            data['banned'] = self.is_banned

        if extra_data:
            data.update(extra_data)
        return data

    def search_users(self, query: str):
        results = User.not_blocked_users(logined_user=self).filter(username__icontains=query)[:10]
        return results


class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followings')
    followee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    followed_at = models.DateTimeField(auto_now_add=True)

    objects = FollowsUserManager()
    admin_objects = models.Manager()

    def __str__(self):
        return f'{self.followee} follows {self.follower}'


class Blocks(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blockers')
    blocked_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blocked_users')

    objects = BlocksUserManager()
    admin_objects = models.Manager()

    def __str__(self):
        return f'{self.blocked_by} blocks {self.user}'


class FollowRequest(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follow_requests_to')
    followee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follow_requests')
    created_at = models.DateTimeField(auto_now_add=True)

    objects = FollowRequestUserManager()
    admin_objects = models.Manager()

    def __str__(self):
        return f'{self.follower} requested to follow {self.followee}'

    def accept(self):
        self.follower.follow(self.followee)
        self.delete()

    def decline(self):
        self.delete()

    def get_context(self, user: 'User'):
        return {
            'follower': self.follower.get_context(logined_user=user),
            'followee': self.followee.get_context(logined_user=user),
        }
