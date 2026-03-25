from django.conf import settings

# Only import S3 storage if AWS is being used
if getattr(settings, 'USE_AWS', False):
    from storages.backends.s3boto3 import S3Boto3Storage

    class StaticStorage(S3Boto3Storage):
        location = settings.STATICFILES_LOCATION

    class MediaStorage(S3Boto3Storage):
        location = settings.MEDIAFILES_LOCATION
else:
    # During development, use Django's default file storage
    from django.core.files.storage import FileSystemStorage

    class StaticStorage(FileSystemStorage):
        pass

    class MediaStorage(FileSystemStorage):
        pass