import os
from io import BytesIO
from typing import BinaryIO, Generator, List

import boto3  # type: ignore

from .protocol import DatalakeProtocol, Result


class S3Client:
    def __init__(self, aws_client) -> None:
        self.client = aws_client

    @staticmethod
    def build() -> "DatalakeProtocol":
        AWS_ACCESS_KEY = os.environ["AWS_ACCESS_KEY"]
        AWS_SECRET_KEY = os.environ["AWS_SECRET_KEY"]
        return S3Client(
            boto3.client(
                "s3",
                aws_access_key_id=AWS_ACCESS_KEY,
                aws_secret_access_key=AWS_SECRET_KEY,
            )
        )

    def download_object(self, bucket_name: str, obj_name, dest_file_path):
        self.client.download_file(bucket_name, obj_name, dest_file_path)

    def download_object_as_file(self, bucket_name: str, obj_name: str) -> BinaryIO:
        data = BytesIO()
        self.client.download_fileobj(bucket_name, obj_name, data)
        data.seek(0)
        return data

    def list_objects(
        self, bucket_name: str, prefix="", continuation_token=None
    ) -> Generator[List[Result], None, None]:
        args = {"Bucket": bucket_name, "Prefix": prefix}
        if continuation_token:
            args["ContinuationToken"] = continuation_token
        data = self.client.list_objects_v2(**args)
        res = data["Contents"]
        if not res:
            return
        yield res
        if data.get("NextContinuationToken") is None:
            return
        yield from self.list_objects(
            bucket_name, prefix=prefix, continuation_token=data["NextContinuationToken"]
        )

    def put_object(self, bucket_name: str, path: str, data: BinaryIO) -> None:
        self.client.put_object(Bucket=bucket_name, Body=data, Key=path)
