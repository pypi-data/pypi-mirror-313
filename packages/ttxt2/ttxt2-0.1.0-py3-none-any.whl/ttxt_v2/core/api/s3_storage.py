import asyncio

import boto3
from botocore.exceptions import ClientError

from ttxt_v2.utils.logger import logger

from .storage_backend import IStorageBackend


class S3StorageBackend(IStorageBackend):
    def __init__(self, bucket_name: str, s3_client=None):
        self.bucket_name = bucket_name
        self.s3_client = s3_client or boto3.client("s3")

    async def write_batch(self, file_name: str, data: bytes):
        loop = asyncio.get_event_loop()
        try:
            await loop.run_in_executor(None, self._upload_to_s3, file_name, data)
            logger.info(f"Wrote data to s3://{self.bucket_name}/{file_name}")
        except ClientError as e:
            logger.error(f"Failed to write batch to S3 {file_name}: {e}")

    def _upload_to_s3(self, file_name: str, data: bytes):
        self.s3_client.put_object(Bucket=self.bucket_name, Key=file_name, Body=data)
