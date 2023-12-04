from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

from Account.models import User


@receiver(post_save, sender=User)
def send_email_verification_link(_: type[User], instance: User, created: bool, **__):
    if created:
        token = default_token_generator.make_token(instance)
        subject = 'Welcome to ConnectionHub world'
        message = f'Hi {instance.username}, thank you for registering in ConnectionHub. Your Token is: {token}.'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [instance.email]
        send_mail(
            subject=subject,
            message=message,
            from_email=email_from,
            recipient_list=recipient_list,
            fail_silently=False
        )
