import uuid
from typing import Optional
from uuid import uuid4

from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, AbstractUser
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.db.models import Model, UUIDField, DateTimeField, CharField, EmailField, BooleanField
from django.utils.translation import gettext_lazy as _

from Account.tokens import Token


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
    id = UUIDField(
        default=uuid4,
        primary_key=True,
        editable=False,
        verbose_name='ID'
    )
    username = CharField(
        _("Username"),
        max_length=150,
        unique=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[AbstractUser.username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
        db_index=True
    )

    phone = CharField(
        _('Phone Number'),
        unique=True
    )
    email = EmailField(
        _("Email Address"),
        unique=True
    )
    is_verified = BooleanField(
        _("Email Verified"),
        default=False,
        help_text=_(
            "Designates whether this user email verified or not. "
            "Unselect this instead of deleting accounts."
        ),
    )

    first_name = None
    last_name = None

    REQUIRED_FIELDS = ["email", "phone"]

    class Meta:
        db_table = 'users'

    def verify_email(self):
        self.is_verified = True
        self.save()

    @property
    def profile_id(self) -> Optional[uuid.UUID]:
        try:
            return self.profile.id
        except ObjectDoesNotExist:
            return None

    def send_verification_email(self):
        token = Token.email_verification_token(user=self)
        subject = 'Welcome to ConnectionHub world'
        message = f'Hi {self.username}, Thank you for registering in ConnectionHub. Your Token is: {str(token)}.'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [self.email]
        send_mail(
            subject=subject,
            message=message,
            from_email=email_from,
            recipient_list=recipient_list,
            fail_silently=False
        )

    def __str__(self):
        return f'@{self.username}'
