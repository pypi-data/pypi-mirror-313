import logging

import boto3

from acryl.executor.cloud_utils.cloud_copier import CloudCopier

logger = logging.getLogger(__name__)


class S3CloudCopier(CloudCopier):
    log = logging.getLogger(__name__)

    def __init__(self, bucket: str, base_path: str) -> None:
        self.bucket = bucket
        self.base_path = base_path
        self.session = boto3.session.Session()

    def upload(self, source_local_file: str, target_cloud_file: str) -> None:
        s3 = self.session.resource("s3")

        key = self.base_path.rstrip("/") + "/" + target_cloud_file.lstrip("/")
        logger.info(
            f"Uploading {source_local_file} to bucket: {self.bucket} and base path {self.base_path} and key {key}"
        )
        s3.meta.client.upload_file(
            Filename=source_local_file,
            Bucket=self.bucket,
            Key=key,
        )
