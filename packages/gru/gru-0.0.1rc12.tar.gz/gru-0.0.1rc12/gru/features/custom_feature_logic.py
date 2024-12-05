from typing import Dict, List


class CustomFeatureLogic:
    """
    Creates CustomFeatureLogic object for the feature logic provided from custom UDF.

    Attributes:
        custom_class_name (str): Class name from custom file.
        file_path (str): File path containing custom UDF script.
        is_feature_logic_custom (bool): Flag to decide weather the logic is custom or predefined, Default value is True.

    Examples
    --------
    >>>     feature_logic=CustomFeatureLogic(
    ...         custom_class_name="CustomClassTestV1",
    ...         file_path="/path/to/custom_file/file.py"
    ...     )
    """

    def __init__(
        self,
        custom_class_name: str = "",
        file_path: str = "",
        timestamp_field: str = "",
        time_window: str = "",
        groupby_keys: List = [],
    ):
        self.custom_class_name = custom_class_name
        self.file_path = file_path
        self.is_feature_logic_custom = True
        self.function_type = "CustomUDF"
        self.timestamp_field = timestamp_field
        self.time_window = time_window
        self.groupby_keys = groupby_keys

    def to_json(self) -> Dict:
        """
        Returns:
            Dict: A dictionary representing the feature attributes in JSON format.
        """
        return {
            "function_type": self.function_type,
            "is_feature_logic_custom": self.is_feature_logic_custom,
            "custom_class_name": self.custom_class_name,
            "file_path": self.file_path,
            "timestamp_field": self.timestamp_field,
            "time_window": self.time_window,
            "groupby_keys": self.groupby_keys
        }
