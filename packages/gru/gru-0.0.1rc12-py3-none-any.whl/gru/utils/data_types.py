"""
Module consisting of classes and functions for Datatypes supported by our platform. Currently all Apache Pyspark SQL datatypes are supported.
Reference: https://sparkbyexamples.com/pyspark/pyspark-sql-types-datatype-with-examples/
"""



from enum import Enum, unique

@unique
class DataType(Enum):
    """
    Enum-like class defining data types supported by our Platform
    """

    INT = "integer"
    STRING = "string"
    TIMESTAMP = "timestamp"
    FLOAT = "float"
    DATETIME = "datetime"
    LIST = "list"
    LIST_INT = "list[integer]"
    LIST_FLOAT = "list[float]"
    LIST_STRING = "list[string]"

    @classmethod
    def get_key(cls, value):
        """
        Get the key (name) of a data type based on its value.

        Args:
            value (str): The value of the data type.

        Returns:
            str: The key (name) of the data type, or None if not found.
        """
        for item in cls:
            if item.value == value:
                return item.name
        return None
