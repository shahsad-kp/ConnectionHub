from django.db.models import ForeignKey, CASCADE, FilePathField, TextField, ManyToManyField, CharField, FileField
from django.utils.translation import gettext_lazy as _

from Account.models import BaseModel, User
from Profile.models import Profile


class Post(BaseModel):
    profile = ForeignKey(
        verbose_name=_('Profile'),
        to=Profile,
        on_delete=CASCADE
    )
    caption = TextField(
        _('Caption'),
        blank=True
    )
    tags = ManyToManyField(
        verbose_name=_('Post Tags'),
        to='Tag',
        blank=True
    )
    location = CharField(
        _('Location'),
        max_length=255,
        blank=True
    )

    class Meta:
        db_table = 'posts'


class PostImage(BaseModel):
    file_name = CharField(
        verbose_name=_('File name')
    )
    post = ForeignKey(
        verbose_name=_('Post'),
        to=Post,
        on_delete=CASCADE,
        related_name='images'
    )

    class Meta:
        db_table = 'post_images'

    def __str__(self):
        return 'Image of {}'.format(str(self.post))

    @property
    def url(self) -> str:
        return f'{self}'

    @property
    def key(self):
        return f'posts/{self.post.profile_id}/{self.post_id}/{self.id}'


class Tag(BaseModel):
    name = CharField(unique=True)

    def __str__(self):
        return f'#{self.name}'

    class Meta:
        db_table = 'tags'
