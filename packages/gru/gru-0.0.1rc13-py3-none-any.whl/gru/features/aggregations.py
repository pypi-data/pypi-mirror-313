"""
Aggregations that can be used to define Features.
Functions for Derived Features
- add
- subtract
- multiply
- safe_divide
- binarize
- bucketize

`Spark's Bucketizer Feature Transformer <https://spark.apache.org/docs/latest/api/python/reference/api/pyspark.ml.feature.Bucketizer.html>`_
"""
import warnings
from typing import Union, List, Dict, Any

# TODO: [RJS 2024-06-20] - Modify the docstring for aggregation functions used for derived feature.


class WindowAggregation:
    """
    WindowAggregation is used for calculating aggregations on given features for a fixed window in streaming data.

    This class supports various aggregation functions and allows for customization of the window parameters.

    Parameters
    ----------
    function : str
        Aggregation function to be performed on the given feature (e.g., "sum", "avg", "max", "min", "count").
    partition_by : str, optional
        Column(s) to partition the data by before applying the window function.
    order_by : str, optional
        Column(s) to order the data by within each partition.
    window_duration : str, optional
        The duration of the window (e.g., "5 seconds", "1 minute", "1 hour").
    watermark_delay_threshold : str, optional
        The maximum time to wait for late data. Events arriving later than this will be dropped.

    Attributes
    ----------
    transform_args : dict
        A dictionary containing all the parameters for the window aggregation, including the function type.

    Examples
    --------
    >>> window_agg = WindowAggregation(
    ...     function="sum",
    ...     partition_by="user_id",
    ...     order_by="timestamp",
    ...     window_duration="5 minutes",
    ...     watermark_delay_threshold="10 seconds"
    ... )

    """
    def __init__(
        self,
        function: str,
        partition_by: str = None,
        order_by: str = None,
        window_duration: str = None,
        watermark_delay_threshold: str = None
    ):
        self.function = function
        self.partition_by = partition_by
        self.order_by = order_by
        self.window_duration = window_duration
        self.watermark_delay_threshold = watermark_delay_threshold
        self.transform_args = {
            "function": self.function,
            "partition_by": self.partition_by,
            "order_by": self.order_by,
            "window_duration": self.window_duration,
            "watermark_delay_threshold": self.watermark_delay_threshold,
            "function_type": "WindowAggregation",
        }


class SlidingWindowAggregation:
    """
    SlidingWindowAggregation is used for calculating aggregations on given features using a sliding window approach
    in both batch and streaming data scenarios.

    This class supports various aggregation functions and allows for customization of the window parameters,
    including range-based windows, row-based windows, and streaming windows.

    Parameters
    ----------
    function : str
        Aggregation function to be performed on the given feature (e.g., "sum", "avg", "max", "min", "count").
    partition_by : str
        Column(s) to partition the data by before applying the window function.
    rangeBetween : Dict, optional
        A dictionary specifying the range-based window. It should contain 'frame_start' and 'frame_end' keys.
    rowsBetween : Dict, optional
        A dictionary specifying the row-based window. It should contain 'frame_start' and 'frame_end' keys.
    window_period : str, optional
        The interval at which the window slides forward (for streaming windows).
    window_duration : str, optional
        The duration of the window (for streaming windows).
    watermark_delay_threshold : str, optional
        The maximum time to wait for late data in streaming scenarios. Events arriving later than this will be dropped.
    order_by : List[str], optional
        Column(s) to order the data by within each partition.

    Attributes
    ----------
    transform_args : dict
        A dictionary containing all the parameters for the sliding window aggregation, including the function type.

    Examples
    --------
     >>> streaming_window = SlidingWindowAggregation(
    ...     function="count",
    ...     partition_by="category",
    ...     order_by=["event_time"],
    ...     window_period="1 minute",
    ...     window_duration="5 minutes",
    ...     watermark_delay_threshold="10 seconds"
    ... )
    """

    def __init__(
        self,
        function: str,
        partition_by: str,
        rangeBetween: Dict = None,
        rowsBetween: Dict = None,
        window_period: str = None,
        window_duration: str = None,
        watermark_delay_threshold: str = "",
        order_by: List[str] = [],
    ):
        warnings.warn(
            "This is currently a partially-implemented feature. If a data source has different folders/keys (e.g. one key for each day or one key for each hour etc.) this may lead to unexpected and inaccurate results. This is because additional data may need to be read to complete the window that has been specified for some rows. A follow-up release will allow the specification of an optional cushion argument, so that each feature job can read additional keys/folders of data to accommodate the window frame provided for all rows."
        )

        self.function = function
        self.partition_by = partition_by
        self.order_by = order_by
        self.rangeBetween = rangeBetween
        self.rowsBetween = rowsBetween
        self.window_period = window_period
        self.window_duration = window_duration
        self.watermark_delay_threshold = watermark_delay_threshold
        if self.rangeBetween is not None:
            frame_start_range = self.frame_start_range_val = self.rangeBetween.get(
                "frame_start"
            )
            frame_end_range = self.frame_end_range_val = self.rangeBetween.get(
                "frame_end"
            )
            self.frame_start_range_exists = frame_start_range is not None
            self.frame_end_range_exists = frame_end_range is not None
            if self._validate_range():
                self._validate_frame_range_valid_window()

        if rowsBetween is not None:
            self.frame_start_rows = self.frame_start_rows_val = rowsBetween.get(
                "frame_start"
            )
            self.frame_end_rows = self.frame_end_rows_val = rowsBetween.get("frame_end")
            self.frame_start_rows_exists = self.frame_start_rows is not None
            self.frame_end_rows_exists = self.frame_end_rows is not None
            if self._validate_rows():
                self._validate_frame_rows_valid_window()

        if window_period != None and window_duration != None:
            self.streaming_slidingwindow_args()

    def _validate_order_by(self, order_by: List[str]) -> bool:
        """
        Validate that the specified order column is not empty.

        Args:
            order_by (List[str]): The name of the column to use for ordering.

        Raises:
            ValueError: If the order_by is empty.

        Returns:
            bool

        """
        if len(order_by) == 0:
            raise ValueError("order_by should not be empty")
        return True

    def _validate_range(self) -> bool:
        """
        Validate that the  start range value  and end range value should not be None.
        Raises:
            ValueError: If frame_start_range and frame_end_range is None .
        Returns:
            bool
        """
        if not self.frame_start_range_exists:
            raise ValueError(
                "Please enter the value of frame_start_range. It should not be null"
            )
        elif not self.frame_end_range_exists:
            raise ValueError(
                "Please enter the value of frame_end_range. It should not be null"
            )
        return (
            self.frame_start_range_exists
            and self.frame_end_range_exists
            and self._validate_order_by(self.order_by)
        )

    def _validate_frame_range_valid_window(self) -> Dict:
        """
        Validate that the  start range value  should be less than equal to  end range value .
        Raises:
            ValueError: If frame_start_range is greater frame_end_range is None .
        Returns:
            dict
        """
        if (
            self.frame_start_range_exists
            and self.frame_end_range_exists
            and (self.frame_start_range_val <= self.frame_end_range_val)
        ):
            self.transform_args = {
                "function": self.function,
                "partition_by": self.partition_by,
                "order_by": self.order_by,
                "rangeBetween": self.rangeBetween,
                "function_type": "SlidingWindowAggregation",
            }
        else:
            raise ValueError(
                "The start value of the range should be smaller than or equal to the end value of the range."
            )

    def streaming_slidingwindow_args(self) -> Dict:
        self.transform_args = {
            "function": self.function,
            "partition_by": self.partition_by,
            "order_by": self.order_by,
            "window_period": self.window_period,
            "window_duration": self.window_duration,
            "watermark_delay_threshold": self.watermark_delay_threshold,
            "function_type": "SlidingWindowAggregation",
        }

    def _validate_rows(self) -> bool:
        """
        Validate that the  start rows value  and end rows value should not be None.
        Raises:
            ValueError: If frame_start_rows and frame_end_rows is None .
        Returns:
            bool
        """
        if not self.frame_start_rows_exists:
            raise ValueError(
                " Please enter the value of frame_start_rows. It should not be null"
            )
        elif not self.frame_end_rows_exists:
            raise ValueError(
                "Please enter the value of frame_end_rows. It should not be null"
            )
        return (
            self.frame_start_rows_exists
            and self.frame_end_rows_exists
            and self._validate_order_by(self.order_by)
        )

    def _validate_frame_rows_valid_window(self) -> Dict:
        """
        Validate that the  start rows value  should be less than equal to  end rows value .
        Raises:
            ValueError: If  value of frame_start_rows is greater than  frame_end_rows.
        Returns:
            dict
        """
        if (
            self.frame_start_rows_exists
            and self.frame_end_rows_exists
            and (self.frame_start_rows_val <= self.frame_end_rows_val)
        ):
            self.transform_args = {
                "function": self.function,
                "partition_by": self.partition_by,
                "order_by": self.order_by,
                "rowsBetween": self.rowsBetween,
                "function_type": "SlidingWindowAggregation",
            }
        else:
            raise ValueError(
                "The start value of the rows should be smaller than or equal to the end value of the rows."
            )


def add(feature_list: List[str], groupby_keys: List[str]) -> Dict[str, Any]:
    """
    Aggregation function to create a derived feature by adding multiple raw/derived features

    Parameters
    ----------
    *args: accepting variable number of feature names

    Returns
    -------
    returns a json object as below:


    >>> {
            "transform": "add",
            "feature_list": ['feature_1', 'feature_2', ...]
        }

    Notes
    -----
    Only feature names will be accepted as arguments

    Examples
    --------

    """

    if not groupby_keys:
        raise ValueError("groupby_keys must contain at least one key")

    obj = {
        "transform": "add",
        "feature_list": feature_list,
        "groupby_keys": groupby_keys,
    }
    return obj


def subtract(feature_list: List[str], groupby_keys: List[str]) -> Dict[str, Any]:
    """
    Aggregation function to create a derived feature by subtracting feature1 from feature2

    Parameters
    ----------
    feature1: string
        name of the feature to be subtracted
    feature2: string
        name of the feature from which we'll subtract

    Returns
    -------
    returns a json object as below:


    >>> {
            "transform": "subtract",
            "feature_list": ['feature_1', 'feature_2']
        }

    Notes
    -----
    Only feature names will be accepted as arguments

    Examples
    --------

    """

    if len(feature_list) != 2:
        raise ValueError(
            "feature_list must contain exactly two elements: ['feature1', 'feature2']"
        )

    if not groupby_keys:
        raise ValueError("groupby_keys must contain at least one key")

    obj = {
        "transform": "subtract",
        "feature_list": feature_list,
        "groupby_keys": groupby_keys,
    }
    return obj


def multiply(feature_list: List[str], groupby_keys: List[str]) -> Dict[str, Any]:
    """
    Aggregation function to create a derived feature by multiplying multiple raw/derived features

    Parameters
    ----------
    *args: accepting variable number of feature names

    Returns
    -------
    returns a json object as below:


    >>> {
            "transform": "multiply",
            "feature_list": ['feature_1', 'feature_2', ...]
        }

    Notes
    -----
    Only feature names will be accepted as arguments

    Examples
    --------

    """
    if not groupby_keys:
        raise ValueError("groupby_keys must contain at least one key")

    obj = {
        "transform": "multiply",
        "feature_list": feature_list,
        "groupby_keys": groupby_keys,
    }
    return obj


def safe_divide(feature_list: List[str], groupby_keys: List[str]) -> Dict[str, Any]:
    """
    Aggregation function to create a derived feature by safe dividing feature1 from feature2

    Parameters
    ----------
    feature1: string
        name of the feature to be divided
    feature2: string
        name of the feature from which we'll divide

    Returns
    -------
    returns a json object as below:


    >>> {
            "transform": "safe_divide",
            "feature_list": ['feature_1', 'feature_2']
        }

    Notes
    -----
    Only feature names will be accepted as arguments

    Examples
    --------

    """
    if len(feature_list) != 2:
        raise ValueError(
            "feature_list must contain exactly two elements: ['feature1', 'feature2']"
        )

    if not groupby_keys:
        raise ValueError("groupby_keys must contain at least one key")

    obj = {
        "transform": "safe_divide",
        "feature_list": feature_list,
        "groupby_keys": groupby_keys,
    }
    return obj


def binarize(
    feature: str,
    threshold: Union[int, float],
    groupby_keys: List,
    if_true: Union[int, float, bool, str] = 1,
    if_false: Union[int, float, bool, str] = 0,
) -> Dict[str, Any]:
    """
    Performs binarization by thresholding numerical features to binary features using Spark's Binarizer Feature Transformer

    Parameters
    ----------
    feature: str
        feature name to binarize
    threshold: Union[int, float]
        threshold value can either be an int or float. Feature will be binarized based on the threshold value
    if_true: Union[int, float, bool, str]
        For feature values greater than threshold, if_true value will be set to the binarize feature. Default set to 1
    if_false: Union[int, float, bool, str]
        For feature values less than threshold, if_false value will be set to the binarize feature. Default set to 0

    Returns
    -------
    returns a json object as below:


    >>> {
            "transform": "binarize",
            "feature_list": [feature],
            feature_transform_args : {
                "labels": [if_true, if_false],
                "threshold": threshold,
            }
        }

    Notes
    -----

    Examples
    --------
    >>> create_derived_feature = CreateDerivedFeature(
    ...     feature_name="player_count_test",
    ...     feature_description="Total players",
    ...     feature_data_type="FLOAT",
    ...     owners=["all-ds@company.com", "temp"],
    ...     schedule="*/7 * * * *",
    ...     entity=["player_count"],
    ...     online=False,
    ...     offline=True,
    ...     transform=src.modules.aggregations.binarize(
    ...         feature = "raw_feature_test",
    ...         threshold = 500,
    ...         if_true = "less",
    ...         if_false = "more"
    ...     ),
    ... )
    """

    if not groupby_keys:
        raise ValueError("groupby_keys must contain at least one key")

    obj = {
        "transform": "binarize",
        "feature_list": [feature],
        "feature_transform_args": {
            "labels": [if_true, if_false],
            "threshold": threshold,
        },
        "groupby_keys": groupby_keys,
    }
    return obj


def bucketize(
    feature: str, groupby_keys: List, splits: List[Union[int, float]], labels: List[str]
) -> Dict[str, Any]:
    """
    Transforms a column of continuous features to a column of feature buckets, where the buckets are specified by users using [Spark's Bucketizer Feature Transformer](https://spark.apache.org/docs/latest/api/python/reference/api/pyspark.ml.feature.Bucketizer.html)

    Parameters
    ----------
    feature: str
        name of the feature to be bucketized
    splits: List[Union[int, float]]
        list of splits based on which a continuous feature will be bucketized
    labels: List[str]
        list of labels that will be assigend as per the splits

    Returns
    -------
    returns a json object as below:


    >>> {
            "transform": "bucketize",
            "feature_list": [feature],
            "feature_transform_args" : {
                "labels": labels,
                "splits": splits,
            }
        }

    Example
    -------
    >>> create_derived_feature = CreateDerivedFeature(
    ...     feature_name="player_count_test",
    ...     feature_description="Total players",
    ...     feature_data_type="FLOAT",
    ...     owners=["all-ds@company.com", "temp"],
    ...     schedule="*/7 * * * *",
    ...     entity=["player_count"],
    ...     online=False,
    ...     offline=True,
    ...     transform=src.modules.aggregations.bucketize(
    ...         feature = "raw_feature_test",
    ...         splits = [-float("inf"), 500, 750, float("inf")],
    ...         labels = ["less_than_500", "greater_than_500","greater_than_750"],
    ...     ),
    ... )
    ... _
    ... create_derived_feature.register_feature()
    ... create_derived_feature.deploy_feature()
    ..."""
    # converting to string for out of range values
    splits_str = [str(split) for split in splits]

    if not groupby_keys:
        raise ValueError("groupby_keys must contain at least one key")

    obj = {
        "transform": "bucketize",
        "feature_list": [feature],
        "feature_transform_args": {
            "labels": labels,
            "splits": splits_str,
        },
        "groupby_keys": groupby_keys,
    }
    return obj


def MIN(feature_list: List[str], groupby_keys: List[str]) -> Dict[str, Any]:
    """
    Aggregation function to create a derived feature by finding the minimum of multiple raw/derived features

    Parameters
    ----------
    *args: accepting variable number of feature names

    Returns
    -------
    returns a json object as below:


    >>> {
            "transform": "min",
            "feature_list": ['feature_1', 'feature_2', ...]
        }

    Notes
    -----
    Only feature names will be accepted as arguments

    Examples
    --------

    """

    if not groupby_keys:
        raise ValueError("groupby_keys must contain at least one key")

    obj = {
        "transform": "min",
        "feature_list": feature_list,
        "groupby_keys": groupby_keys,
    }
    return obj


def MAX(feature_list: List[str], groupby_keys: List[str]) -> Dict[str, Any]:
    """
    Aggregation function to create a derived feature by finding the maximum of multiple raw/derived features

    Parameters
    ----------
    *args: accepting variable number of feature names

    Returns
    -------
    returns a json object as below:


    >>> {
            "transform": "max",
            "feature_list": ['feature_1', 'feature_2', ...]
        }

    Notes
    -----
    Only feature names will be accepted as arguments

    Examples
    --------

    """

    if not groupby_keys:
        raise ValueError("groupby_keys must contain at least one key")

    obj = {
        "transform": "max",
        "feature_list": feature_list,
        "groupby_keys": groupby_keys,
    }
    return obj


def AVG(feature_list: List[str], groupby_keys: List[str]) -> Dict[str, Any]:
    """
    Aggregation function to create a derived feature by calculating the average of multiple raw/derived features

    Parameters
    ----------
    *args: accepting variable number of feature names

    Returns
    -------
    returns a json object as below:


    >>> {
            "transform": "avg",
            "feature_list": ['feature_1', 'feature_2', ...]
        }

    Notes
    -----
    Only feature names will be accepted as arguments

    Examples
    --------

    """

    if not groupby_keys:
        raise ValueError("groupby_keys must contain at least one key")

    obj = {
        "transform": "avg",
        "feature_list": feature_list,
        "groupby_keys": groupby_keys,
    }
    return obj
