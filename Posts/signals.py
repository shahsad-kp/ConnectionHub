from typing import Type

from django.db.models.signals import post_save, post_delete

from Notifications.models import Notification
from Posts.models import Reaction


def pre_like_dislike(sender: Type[Reaction], instance: Reaction, created: bool, **kwargs):
    if created:
        if instance.reaction == 'like':
            instance.post.likes_count += 1
            if not instance.post.user == instance.user:
                Notification.create_notification(
                    recipient=instance.post.user,
                    notification_type='like',
                    content=f'{instance.user} liked your post',
                    arg_value=str(instance.post.id)
                )
        else:
            instance.post.dislikes_count += 1
        instance.post.save()
    else:
        if instance._old_reaction != instance.reaction:
            if instance.reaction == 'like':
                instance.post.likes_count += 1
                instance.post.dislikes_count -= 1
                if not instance.post.user == instance.user:
                    Notification.create_notification(
                        recipient=instance.post.user,
                        notification_type='like',
                        content=f'{instance.user} liked your post',
                        arg_value=str(instance.post.id)
                    )
            else:
                instance.post.dislikes_count += 1
                instance.post.likes_count -= 1
            instance.post.save()


def delete_like_dislike(sender: Type[Reaction], instance: Reaction, **kwargs):
    if instance.reaction == 'like':
        instance.post.likes_count = instance.post.likes_count - 1
    else:
        instance.post.dislikes_count = instance.post.dislikes_count - 1
    instance.post.save()


post_save.connect(pre_like_dislike, sender=Reaction)
post_delete.connect(delete_like_dislike, sender=Reaction)
