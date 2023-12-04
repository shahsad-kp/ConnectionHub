from django.db.models import CharField, ImageField, TextField, OneToOneField, CASCADE
from django.utils.translation import gettext_lazy as _

from Account.models import BaseModel, User


class Profile(BaseModel):
    user = OneToOneField(
        to=User,
        related_name='profile',
        on_delete=CASCADE
    )
    first_name = CharField(
        _('First name'),
        max_length=255
    )
    last_name = CharField(
        _('Last name'),
        max_length=255
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
        return self.full_name

    @property
    def full_name(self) -> str:
        return f'{self.first_name} {self.last_name}'
