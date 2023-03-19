from django.db.models.signals import post_save
from django.dispatch import receiver

from Users.models import User
from UsersSettings.models import UserSettings


@receiver(post_save, sender=User)
def create_user_settings(sender, instance, created, **kwargs):
    if created:
        UserSettings.objects.create(user=instance)