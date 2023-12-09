from django.core.exceptions import ValidationError
from django.db.models import (
    CharField,
    ImageField,
    TextField,
    OneToOneField,
    CASCADE,
    ForeignKey
)
from django.utils.translation import gettext_lazy as _

from Account.models import BaseModel, User


class Profile(BaseModel):
    user = OneToOneField(
        to=User,
        related_name='profile',
        on_delete=CASCADE,
        db_index=True
    )
    first_name = CharField(
        _('First name'),
        max_length=255,
        blank=True
    )
    last_name = CharField(
        _('Last name'),
        max_length=255,
        blank=True
    )
    profile_picture = ImageField(
        _('Profile Picture'),
        upload_to='profile_picture/',
        blank=True
    )
    about = TextField(
        _('About text'),
        blank=True,
    )

    class Meta:
        db_table = 'profiles'

    def __str__(self):
        return f'Profile of {self.user}'

    @property
    def full_name(self) -> str:
        return f'{self.first_name} {self.last_name}'

    def follow(self, profile: 'Profile'):
        return self.followers.create(
            follower=profile
        )


class Follow(BaseModel):
    follower = ForeignKey(
        verbose_name=_('Follower'),
        to=Profile,
        on_delete=CASCADE,
        related_name='followings'
    )
    followee = ForeignKey(
        verbose_name=_('Followee'),
        to=Profile,
        on_delete=CASCADE,
        related_name='followers'
    )

    class Meta:
        db_table = 'follows'
        unique_together = ('follower', 'followee',)

    def __str__(self):
        return f'{self.follower} follows {self.followee}'

    def clean(self):
        if self.follower == self.followee:
            raise ValidationError(_('Follower and Followee cannot be the same.'))
