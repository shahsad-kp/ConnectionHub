from typing import Type

from django.core.mail import EmailMessage
from django.db.models.signals import post_save, pre_save, post_delete
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


@receiver(post_delete, sender=Follow)
def unfollow_signal(sender: Type[Follow], instance: Follow, **kwargs):
    instance.followee.followers_count -= 1
    instance.follower.followings_count -= 1
    instance.followee.save()
    instance.follower.save()


@receiver(pre_save, sender=User)
def user_updated(sender, **kwargs):
    user = kwargs.get('instance', None)
    if user:
        new_password = user.password
        try:
            old_password = User.objects.get(pk=user.pk).password
        except User.DoesNotExist:
            old_password = None
        if new_password != old_password:
            message = EmailMessage(
                subject='Password Changed Successfully',
                body=f"""Dear @{user.username},

We are writing to inform you that your password for ConnectionHub account has been successfully changed.

We understand that changing your password can be an inconvenience, but it is an important security measure that helps 
protect your account from unauthorized access. If you did not initiate this change or suspect any unauthorized access 
to your account, please contact our customer support team immediately.

Please remember to keep your new password secure and confidential. Avoid using easily guessable information such as 
your name or date of birth, and ensure that your password is a combination of letters, numbers, and special characters.

If you experience any difficulties accessing your account with the new password, please let us know and we will be 
happy to assist you.

Thank you for using ConnectionHub. We appreciate your continued trust and support.

Best regards,

Customer Support

ConnectionHub""",
                to=[user.email]
            )
            message.send(fail_silently=True)
