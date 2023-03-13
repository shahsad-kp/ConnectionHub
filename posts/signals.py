from typing import Type

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from Notifications.models import Notification
from Posts.models import Reaction


@receiver(post_save, sender=Reaction)
def post_like_dislike(sender: Type[Reaction], instance: Reaction, created: bool, **kwargs):
    if created:
        if instance.reaction == 'like':
            instance.post.likes_count += 1
            if not instance.post.user == instance.user:
                Notification.create_notification(
                    recipient=instance.post.user,
                    notification_type='like',
                    content=f'@{instance.user} liked your post',
                    arg_value=str(instance.post.id)
                )
        else:
            instance.post.dislikes_count += 1
        instance.post.save()


@receiver(post_delete, sender=Reaction)
def post_like_dislike(sender: Type[Reaction], instance: Reaction, **kwargs):
    if instance.reaction == 'like':
        instance.post.likes_count -= 1
    else:
        instance.post.dislikes_count -= 1
    instance.post.save()
