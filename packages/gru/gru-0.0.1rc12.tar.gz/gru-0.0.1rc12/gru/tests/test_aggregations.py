import unittest

from gru.features.aggregations import SlidingWindowAggregation

obj = SlidingWindowAggregation(
    function="AVG",
    partition_by="provider",
    order_by=["project_id"],
    rangeBetween={"frame_start": 1, "frame_end": 6},
)


def _validate_frame_range_valid_window(
    frame_start_range_exists,
    frame_end_range_exists,
    frame_start_range_val,
    frame_end_range_val,
):
    """
    Validate that the  start range value  should be less than equal to  end range value .

    Raises:
        ValueError: If frame_start_range is greater frame_end_range is None .

    Returns:
        dict

    """
    if (
        frame_start_range_exists
        and frame_end_range_exists
        and (frame_start_range_val <= frame_end_range_val)
    ):
        return {
            "function": "AVG",
            "partition_by": "provider",
            "order_by": ["order_by"],
            "rangeBetween": {"frame_start": 1, "frame_end": 2},
        }
    else:
        raise ValueError(
            "The start value of the range should be smaller than or equal to the end value of the range."
        )


class Test(unittest.TestCase):
    def test_validate_order_by1(self):
        """
        Unittest to ensure order_by list is not empty
        """
        order_by = ["project_id"]
        result = obj._validate_order_by(order_by)
        self.assertEqual(result, True)

    def test_validate_order_by2(self):
        """
        Unittest to check if order_by is empty
        """
        order_by = []
        with self.assertRaises(ValueError):
            result = obj._validate_order_by(order_by)

    def test_validate_range1(self):
        """
        Unittest to validate the range for range_between
        """
        result = obj._validate_range()
        self.assertEqual(result, True)

    def test_validate_frame_range_valid_window2(self):
        """
        Evaluating if  value error is raised given any one of parameter is False.
        """
        with self.assertRaises(ValueError):
            result = _validate_frame_range_valid_window(True, False, 1, 2)

    def test_validate_frame_range_valid_window2(self):
        """
        Checking if the return value is dict or not
        """
        transform_args = {
            "function": "AVG",
            "partition_by": "provider",
            "order_by": ["order_by"],
            "rangeBetween": {"frame_start": 1, "frame_end": 2},
        }
        result = _validate_frame_range_valid_window(True, True, 1, 2)
        self.assertDictEqual(result, transform_args)

    def test_validate_frame_range_valid_window3(self):
        """
        Evaluating if  value error is raised given any one of parameter is False
        """
        with self.assertRaises(ValueError):
            result = _validate_frame_range_valid_window(False, False, 1, 2)


if __name__ == "__main__":
    unittest.main()
