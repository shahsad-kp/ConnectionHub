from typing import Type

from django.core.mail import EmailMessage
from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from django.template.loader import render_to_string

from Notifications.models import Notification
from Users.models import User, Follow

PASSWORD_CHANGED_MESSAGE = '''We are writing to inform you that your password for ConnectionHub account has been \
successfully changed.

We understand that changing your password can be an inconvenience, but it is an important security measure that helps \
protect your account from unauthorized access. If you did not initiate this change or suspect any unauthorized access \
to your account, please contact our customer support team immediately.

Please remember to keep your new password secure and confidential. Avoid using easily guessable information such as \
your name or date of birth, and ensure that your password is a combination of letters, numbers, and special characters.

If you experience any difficulties accessing your account with the new password, please let us know and we will be \
happy to assist you.

Thank you for using ConnectionHub. We appreciate your continued trust and support.'''

WELCOME_MESSAGE = '''We're thrilled to have you join our social network app and become part of our community. As a new\
 user, we want to make sure you feel welcome and comfortable exploring all the features our app has to offer.

Whether you're looking to connect with friends, meet new people, or simply discover new content, our app has something \
for everyone. We believe that our community is only as strong as its members, so we're excited to have you on board and\
 can't wait to see what you'll bring to the table.

If you have any questions, concerns, or feedback, please don't hesitate to reach out to our support team. We're always \
here to help and want to ensure that your experience on our app is nothing short of exceptional.

Thank you for joining us and we hope you enjoy your time on ConnectionHub!'''

USERNAME_CHANGED_MESSAGE = '''We're writing to confirm that your username has been successfully updated on \
ConnectionHub. Your new username is @{username}.  

If you didn't authorize this change or have any concerns about your account, please contact us immediately.

Thank you for being a valued member of our community.'''


@receiver(post_save, sender=User)
def welcome_notification(sender: Type[User], instance: User, created: bool, **kwargs):
    if created:
        Notification.create_notification(
            recipient=instance,
            notification_type='welcome',
            content='Welcome to our community!'
        )
        subject = 'Welcome to ConnectionHub'
        html_message = render_to_string(
            'email-template.html',
            {
                'name': instance.full_name,
                'message': WELCOME_MESSAGE
            }
        )
        message = EmailMessage(
            subject=subject,
            body=html_message,
            to=[instance.email],
        )
        message.content_subtype = 'html'
        message.send(fail_silently=True)


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
            content=f'{instance.follower} started following you',
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
    user: User = kwargs.get('instance', None)
    if not user:
        return
    if not User.objects.filter(pk=user.pk).exists():
        return

    new_password = user.password
    new_username = user.username

    try:
        old_password = User.objects.get(pk=user.pk).password
        old_username = User.objects.get(pk=user.pk).username
    except User.DoesNotExist:
        old_password = None
        old_username = None

    if new_password != old_password:
        subject = 'Your password is changed'
        html_message = render_to_string(
            'email-template.html',
            {
                'name': user.full_name,
                'message': PASSWORD_CHANGED_MESSAGE
            }
        )
        message = EmailMessage(
            subject=subject,
            body=html_message,
            to=[user.email],
        )
        message.content_subtype = 'html'
        message.send(fail_silently=True)

    if new_username != old_username:
        subject = 'Your username is changed'
        html_message = render_to_string(
            'email-template.html',
            {
                'name': user.full_name,
                'message': USERNAME_CHANGED_MESSAGE.format(username=new_username)
            }
        )
        message = EmailMessage(
            subject=subject,
            body=html_message,
            to=[user.email],
        )
        message.content_subtype = 'html'
        message.send(fail_silently=True)
