from uuid import uuid4

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db.models import Model, UUIDField, DateTimeField, CharField, EmailField, ImageField, BooleanField
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class BaseModel(Model):
    id = UUIDField(
        default=uuid4,
        primary_key=True,
        editable=False,
        verbose_name='ID'
    )
    created_at = DateTimeField(
        auto_now_add=True,
        editable=False,
    )
    updated_at = DateTimeField(
        auto_now=True,
        editable=False
    )

    class Meta:
        abstract = True

    def __str__(self):
        return f'{self.id}'


class User(AbstractUser, PermissionsMixin):
    full_name = CharField(
        _('Full Name'),
        max_length=150,
        blank=False
    )
    profile_picture = ImageField(
        _('Profile Picture'),
        upload_to='profile_picture/',
        blank=True,
    )
    phone = CharField(
        _('Phone Number')
    )

    first_name = None
    last_name = None

    REQUIRED_FIELDS = ["full_name", "email", "phone"]

    class Meta:
        db_table = 'users'
