from abc import ABC, abstractmethod
from typing import Any, Dict


class ReadOptions(ABC):
    @abstractmethod
    def to_json(self) -> Dict[str, Any]:
        pass


class KafkaReadOptions(ReadOptions):
    def __init__(
        self,
        watermark_delay_threshold=None,
        processing_time=None,
        starting_timestamp=None,
        starting_offsets_by_timestamp=None,
        starting_offsets=None,
        fail_on_data_loss=False,
        include_headers=None,
        infer_schema=True,
        delimiter="|",
    ):
        self.watermark_delay_threshold = watermark_delay_threshold
        self.processing_time = processing_time
        self.starting_timestamp = starting_timestamp
        self.starting_offsets_by_timestamp = starting_offsets_by_timestamp
        self.starting_offsets = starting_offsets
        self.fail_on_data_loss = fail_on_data_loss
        self.include_headers = include_headers
        self.infer_schema = infer_schema
        self.delimiter = delimiter

    def to_json(self) -> Dict[str, Any]:
        return {
            "watermark_delay_threshold": self.watermark_delay_threshold,
            "processing_time": self.processing_time,
            "starting_timestamp": self.starting_timestamp,
            "starting_offsets_by_timestamp": self.starting_offsets_by_timestamp,
            "starting_offsets": self.starting_offsets,
            "fail_on_data_loss": self.fail_on_data_loss,
            "include_headers": self.include_headers,
            "infer_schema": self.infer_schema,
            "delimiter": self.delimiter,
        }
