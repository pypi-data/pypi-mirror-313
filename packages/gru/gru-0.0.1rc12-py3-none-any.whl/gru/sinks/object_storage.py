"""
Sink Module for Object Storage
"""

from typing import Dict, Optional, Any, Union
from gru.sinks.sink import Sink
from gru.sinks.sink_family import SinkFamily
from gru.utils.cloud_providers import CloudProviders
from gru.sources.file_types import CSVType, ParquetType
from datetime import datetime


class ObjectStorageSink(Sink):
    """A Sink which writes data to Object Storage"""

    def __init__(
        self,
        name: str,
        uri_scheme: str,
        uri_scheme_spark: str,
        bucket: str,
        leading_key: str,
        file_type: Union[CSVType, ParquetType],
        ts_suffix_key: str = "%Y-%m-%d-%H-%M",
        file_type_properties: Optional[Dict[str, Any]] = {},
        created_at=datetime.now(),
        **kwargs,
    ) -> None:
        """
        Initialize the ObjectStorageSink

        :param bucket: The bucket to write files to.
        :param leading_key: The key to write files to.
        :param file_type: The format of the file i.e. CSV, Parquet etc
        :param file_type_properties: The properties of the file format.
        :param ts_suffix_key: An optional timestamped suffix
            (e.g. %Y-%m-%d-%H-%M or d=%Y-%m-%d/h=%H-%M)
        """
        self._check_non_empty_bucket_and_key(bucket, leading_key)

        super().__init__(
            name=name,
            family=SinkFamily.OBJECT_STORAGE.value,
            physical_uri={
                "bucket": bucket,
                "leading_key": leading_key,
                "ts_suffix_key": ts_suffix_key,
            },
            **kwargs,
        )
        self.uri_scheme = uri_scheme
        self.uri_scheme_spark = uri_scheme_spark
        self.file_type = file_type
        self.file_type_properties = file_type_properties

        self.physical_uri["uri_scheme"] = self.uri_scheme
        self.physical_uri["uri_scheme_spark"] = self.uri_scheme_spark
        self.created_at = created_at

    @classmethod
    def _check_non_empty_bucket_and_key(cls, bucket: str, leading_key: str) -> None:
        """
        Validate that the bucket and leading key are not empty.

        :param bucket: The bucket name.
        :param leading_key: The leading key.
        :raises ValueError: If the bucket or leading key is empty.
        """
        if not bucket:
            raise ValueError("Bucket cannot be empty")
        if not leading_key:
            raise ValueError("Leading key cannot be empty")

    def to_json(self) -> Dict:
        """
        Convert the ObjectStorageSink object to a JSON dictionary.

        :return: The JSON representation of the object.
        """
        return {
            "name": self.name,
            "family": self.family,
            "physical_uri": self.physical_uri,
            "type": self.type,
            "file_type": self.file_type.type if self.file_type else None,
            "file_type_properties": self.file_type.options if self.file_type else None,
            "cloud_provider": self.cloud_provider.value,
            "description": self.description,
            "metadata": self.metadata,
            "owners": self.owners,
            "created_at": str(self.created_at),
        }

    @classmethod
    def from_json(cls, json_dict: Dict) -> "ObjectStorageSink":
        """
        Create an ObjectStorageSink object from a JSON dictionary.

        :param json_dict: The JSON representation of the object.
        :return: The ObjectStorageSink object.
        :raises KeyError: If any required key is missing from the JSON dictionary.
        :raises ValueError: If the bucket or leading key is empty.
        """
        uri_scheme = json_dict["uri_scheme"]
        uri_scheme_spark = json_dict["uri_scheme_spark"]
        bucket = json_dict["bucket"]
        leading_key = json_dict["leading_key"]
        ts_suffix_key = json_dict["ts_suffix_key"]
        file_type = json_dict["file_type"]
        file_type_properties = json_dict["file_type_properties"]

        cls._check_non_empty_bucket_and_key(bucket, leading_key)

        return ObjectStorageSink(
            uri_scheme=uri_scheme,
            uri_scheme_spark=uri_scheme_spark,
            bucket=bucket,
            leading_key=leading_key,
            ts_suffix_key=ts_suffix_key,
            file_type=file_type,
            file_type_properties=file_type_properties,
        )


class S3Sink(ObjectStorageSink):
    """
    A Sink which writes data to AWS S3.

    Parameters:
    - bucket (str): The name of the bucket to write files to.
    - leading_key (str): The leading key to write files to.
    - file_type (str): The format of the file, e.g., CSV, Parquet, etc.
    - ts_suffix_key (str): An optional timestamped suffix for file names (default: "%Y-%m-%d-%H-%M").
    - file_type_properties (Optional[Dict[str, Any]]): The properties of the file format (default: None).

    Inherits:
    - ObjectStorageSink: The base class for writing data to object storage.

    Attributes:
    - cloud_provider (str): The cloud provider.
    - uri_scheme (str): The URI scheme for S3.
    - uri_scheme_spark (str): The URI scheme for Spark to access S3.
    """

    def __init__(
        self,
        name: str,
        bucket: str,
        leading_key: str,
        file_type: Union[CSVType, ParquetType],
        ts_suffix_key: str = "%Y-%m-%d-%H-%M",
        cloud_provider=CloudProviders.AWS,
        file_type_properties: Optional[Dict[str, Any]] = None,
        created_at=datetime.now(),
        **kwargs,
    ) -> None:
        super().__init__(
            name=name,
            uri_scheme="s3",
            uri_scheme_spark="s3a",
            bucket=bucket,
            leading_key=leading_key,
            file_type=file_type,
            ts_suffix_key=ts_suffix_key,
            file_type_properties=file_type_properties,
            type="S3Sink",
            **kwargs,
        )
        self.leading_key = leading_key
        self.cloud_provider = cloud_provider
        self.file_type = file_type
        self.file_type_properties = file_type_properties
        self.created_at = created_at
