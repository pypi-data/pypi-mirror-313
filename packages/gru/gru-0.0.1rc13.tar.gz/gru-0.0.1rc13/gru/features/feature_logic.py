from typing import Dict, List
from gru.features.aggregations import SlidingWindowAggregation, WindowAggregation
from gru.features.transformations import BuiltInTransformation, LambdaTransformation


class FeatureLogic:
    """
    Create a FeatureLogic object for the feature definition

    Parameters
    ----------
    self: str
        self object of the class is the first argument
    field: str
        field on which raw feature will be calculated
    aggregation_fn: str
        aggregation function to be performed on the field
    time_window: str
        time window of the data to be fetched from the data source
    groupby_keys: str
        select fields based on which feature will be calculated
    timestamp_field: str
        timestamp field present in the data source for feature calculation
    timestamp_format: str
        format of the timestamp field
    filter: str
        filter expression that will be applied to rows in the data before performing aggregations. This should be a string and a valid Spark SQL Expression. This is similar to PySpark filter operation, See more details in the official documentation: https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.DataFrame.filter.html
    name: str
        name of the feature logic, default set to ""
    is_feature_logic_custom: bool
        Flag to decide weather the logic is custom or predefined, Default value is True .

    Returns
    -------
    None

    Notes
    -----

    Examples
    --------
    >>>     feature_logic=FeatureLogic(
    ...         name="total_players",
    ...         field=["CASE WHEN cpi> 0.5 THEN 10 ELSE 0 END"],
    ...         aggregation_fn="SUM",
    ...         time_window= "2d",
    ...         groupby_keys=["project_id", "ad_id"],
    ...         timestamp_field="etl_day",
    ...         timestamp_format = "%Y-%m-%d %H:%M"
    ...     )
    """

    def __init__(
        self,
        name: str = "",
        field: List = "",
        transform: object = None,
        time_window: str = "",
        groupby_keys: List = [],
        timestamp_field: str = "",
        timestamp_format: str = "",
        filter: str = None,
    ):
        self.name = name
        self.filter = filter
        self.field = field

        if isinstance(transform, WindowAggregation) or isinstance(
            transform, SlidingWindowAggregation
        ):
            self.transform = transform.transform_args
        elif isinstance(transform, BuiltInTransformation):
            self.transform = transform.to_dict()
        elif isinstance(transform,LambdaTransformation):
            self.transform=transform.to_dict()

        self.time_window = time_window
        self.groupby_keys = groupby_keys
        self.timestamp_field = timestamp_field
        self.timestamp_format = timestamp_format
        self.is_feature_logic_custom = False

    def to_json(self) -> Dict:
        """
        Returns a json-formatted object representing this entity.
        """
        return {
            "name": self.name,
            "transform": self.transform,
            "time_window": self.time_window,
            "groupby_keys": self.groupby_keys,
            "field": self.field,
            "filter": self.filter,
            "timestamp_field": self.timestamp_field,
            "timestamp_format": self.timestamp_format,
            "is_feature_logic_custom": self.is_feature_logic_custom
        }
