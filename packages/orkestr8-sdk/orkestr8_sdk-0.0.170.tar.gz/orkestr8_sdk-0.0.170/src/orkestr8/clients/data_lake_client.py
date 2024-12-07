import logging
from contextlib import contextmanager
from enum import Enum
from typing import BinaryIO, TypeVar

from .protocol import DatalakeProtocol
from .s3 import S3Client

logger = logging.getLogger()


class ClientType(str, Enum):
    S3 = "s3"


CLIENT_TYPE_MAPPING = {ClientType.S3: S3Client}

Client = TypeVar("Client")


class DataLakeClient:
    """'Bucket' client class"""

    def __init__(self, _type: ClientType, bucket_name: str):
        self.client = self.__create_client(_type)
        self.bucket = bucket_name

    def __create_client(self, _type: ClientType) -> DatalakeProtocol:
        """Returns a client based on specific type

        Options are:
            S3

        Raises exception if client not correct type
        """
        if ClientType(_type) == ClientType.S3:
            return CLIENT_TYPE_MAPPING[ClientType.S3].build()
        raise Exception(f"No client configured for '{_type}'")

    def get_object(self, remote_file_path: str, dest_file_path: str) -> None:
        """Retrieves an object from the remote bucket using the `obj_name` and
        saves this object to the `dest_file_path`"""
        logger.info(f"Transerfing '{remote_file_path}' to '{dest_file_path}'")
        self.client.download_object(self.bucket, remote_file_path, dest_file_path)

    @contextmanager
    def get_object_as_file(self, remote_file_path: str):
        """Retrieves an object from the remote bucket using the `obj_name`.
        This will return a ready to use in-memory file-like object. File will
        be closed when ctx manager exits"""

        try:
            data = self.client.download_object_as_file(self.bucket, remote_file_path)
            yield data
        except Exception as e:
            _log = f"Failed to download {remote_file_path}: {str(e)}"
            logger.warning(_log)
            yield None
        else:
            data.close()

    def list_objects(self, prefix=""):
        """Generator to return all objects in a bucket. Yields a list of Result objects"""
        yield from self.client.list_objects(self.bucket, prefix=prefix)

    def put_object(self, path: str, data: BinaryIO):
        """Adds an object to the bucket while implmementing versioning"""
        self.client.put_object(self.bucket, path, data)
