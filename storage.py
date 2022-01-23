from storages.backends.s3boto3 import S3Boto3Storage


class NonPackagingS3PipelineCachedStorage(
    # TODO: fix django pipline, collect static was giving error -- maybe wait until the next release
    # NonPackagingMixin, PipelineMixin, CachedFilesMixin,
    S3Boto3Storage):
    location = 'static'


class MediaStorage(S3Boto3Storage):
    location = 'media'
