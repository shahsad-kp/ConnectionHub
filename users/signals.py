from typing import Type

from django.db.models.signals import post_save
from django.dispatch import receiver

from Notifications.models import Notification
from Users.models import Follow, User


@receiver(post_save, sender=User)
def welcome_notification(sender: Type[User], instance: User, created: bool, **kwargs):
    if created:
        Notification.create_notification(
            recipient=instance,
            notification_type='welcome',
            content='Welcome to our community!'
        )


@receiver(post_save, sender=Follow)
def follow_signal(sender: Type[Follow], instance: Follow, created: bool, **kwargs):
    if created:
        instance.followee.followers_count += 1
        instance.followee.save()
        instance.follower.followings_count += 1
        instance.follower.save()

        Notification.create_notification(
            recipient=instance.followee,
            notification_type='follow',
            content=f'@{instance.follower} started following you',
            arg_value=str(instance.follower.username)
        )
