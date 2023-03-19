from django.db import models

from Users.models import User


class UserSettings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='settings')
    private_account = models.BooleanField(default=False, blank=False)

    def __str__(self):
        return f"Settings of {self.user}"
