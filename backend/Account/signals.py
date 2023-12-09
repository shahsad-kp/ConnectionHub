from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from Account.models import User
from Profile.models import Profile


@receiver(post_save, sender=User)
def user_post_signal(sender: type[User], instance: User, created: bool, **kwargs):
    if created:
        instance.send_verification_email()
        Profile.objects.create(
            user=instance
        )


@receiver(pre_save, sender=User)
def user_pre_signal(sender: type[User], instance: User, **kwargs):
    try:
        original_user = User.objects.get(pk=instance.pk)
        if instance.email != original_user.email:
            instance.is_verified = False
            instance.send_verification_email()
    except User.DoesNotExist:
        pass
