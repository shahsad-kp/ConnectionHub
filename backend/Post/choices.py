from django.db.models import IntegerChoices


class UploadingStatus(IntegerChoices):
    UPLOADING = 1
    UPLOADED = 2
