from functools import cached_property
from io import BytesIO

import boto3

from reach_commons.app_logging.logger import get_reach_logger


class S3Client:
    def __init__(
        self,
        logger=get_reach_logger(),
        region_name="us-east-1",
        profile_name=None,
    ):
        self.logger = logger
        self.region_name = region_name
        self.profile_name = profile_name

    @cached_property
    def client(self):
        session = boto3.Session(
            region_name=self.region_name, profile_name=self.profile_name
        )

        return session.client("s3")

    def get_object(self, s3_bucket_name, s3_key):
        try:
            s3_object = self.client.get_object(Bucket=s3_bucket_name, Key=s3_key)
            actual_message_body = s3_object["Body"].read().decode("utf-8")

            self.logger.info(
                f"Retrieved object from S3: {s3_key} from bucket: {s3_bucket_name}"
            )
            return actual_message_body
        except Exception as e:
            self.logger.error(
                f"Error retrieving object {s3_key} from bucket: {s3_bucket_name}: {str(e)}"
            )

        return None

    def add_object(self, s3_bucket_name, s3_key, str_content):
        try:
            file_object = BytesIO(str_content.encode("utf-8"))

            self.client.upload_fileobj(
                Fileobj=file_object, Bucket=s3_bucket_name, Key=s3_key
            )
            url = (
                f"https://{s3_bucket_name}.s3.{self.region_name}.amazonaws.com/{s3_key}"
            )

            self.logger.info(
                f"Uploaded object to S3: {s3_key} in bucket: {s3_bucket_name}"
            )
            return url
        except Exception as e:
            self.logger.error(
                f"Error uploading object {s3_key} to bucket: {s3_bucket_name}: {str(e)}"
            )
            return None
