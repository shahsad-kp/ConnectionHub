from django.db.models import ForeignKey, CASCADE, FilePathField, TextField, ManyToManyField, CharField, FileField
from django.utils.translation import gettext_lazy as _

from Account.models import BaseModel, User
from Post.choices import UploadingStatus
from Profile.models import Profile
from utils.s3_storage import generate_presigned_url_get, generate_presigned_url_put


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
    status = CharField(
        verbose_name=_('File uploading status'),
        choices=UploadingStatus.choices,
        default=UploadingStatus.UPLOADING
    )

    class Meta:
        db_table = 'post_images'

    def __str__(self):
        return 'Image of {}'.format(str(self.post))

    @property
    def key(self):
        return f'posts/{self.post.profile_id}/{self.post_id}/{self.id}'

    @property
    def get_url(self) -> str:
        return generate_presigned_url_get(self.key)

    @property
    def put_url(self) -> str:
        return generate_presigned_url_put(self.key)


class Tag(BaseModel):
    name = CharField(unique=True)

    def __str__(self):
        return f'#{self.name}'

    class Meta:
        db_table = 'tags'
