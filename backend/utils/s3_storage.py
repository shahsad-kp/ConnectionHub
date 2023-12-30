import hmac
from tempfile import NamedTemporaryFile

from boto3 import resource, session as _session
from django.conf import settings
from storages.backends.s3 import S3Storage

session = _session.Session(region_name=settings.AWS_BUCKET_REGION)

s3 = session.client(
    "s3",
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    config=_session.Config(signature_version="s3v4"),
)


def _get_digest(msg):
    result = hmac.new(
        settings.AWS_SECRET_ACCESS_KEY.encode("utf-8"),
        msg=msg.encode("utf-8"),
        digestmod="md5",
    )
    return result.hexdigest()


def generate_presigned_url(key, method):
    """Generate presigned url for given method."""
    return s3.generate_presigned_url(
        method,
        Params={"Bucket": settings.AWS_BUCKET_NAME, "Key": key},
        ExpiresIn=settings.AWS_EXPIRY,
    )


def generate_presigned_url_public_bucket(key, method="put_object"):
    """Generate presigned url to public bucket for given method."""
    return s3.generate_presigned_url(
        method,
        Params={"Bucket": settings.AWS_PUBLIC_BUCKET_NAME, "Key": key},
        ExpiresIn=settings.AWS_EXPIRY,
    )


def generate_presigned_url_get(key):
    """Generate presigned URL for put_object."""
    return generate_presigned_url(key, "get_object")


def generate_presigned_url_put(key):
    """Generate presigned URL for put_object."""
    return generate_presigned_url(key, "put_object")


def verify_digest(key, digest):
    """Verify the giben digest."""
    return hmac.compare_digest(digest, _get_digest(key))


def delete_objects(key):
    """Delete objects from bucket."""
    s3_resource = resource("s3")
    s3_object = s3_resource.Object(settings.AWS_BUCKET_NAME, key)
    return s3_object.delete()


def upload_file(key, file_obj):
    return s3.upload_fileobj(file_obj, settings.AWS_BUCKET_NAME, key)


def download_file(key):
    file = NamedTemporaryFile(delete=False)
    s3.download_fileobj(settings.AWS_BUCKET_NAME, key, file)
    file.seek(0)
    return file


class StaticS3Storage(S3Storage):
    location = "static"
    default_acl = "public-read"


class MediaS3Storage(S3Storage):
    location = "media"
    file_overwrite = False
