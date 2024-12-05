from abc import ABC, abstractmethod
from typing import Any


class Operation(ABC):
    """
    Abstract class defining the contract for all operations that can be run in different processing engines.

    This abstract class serves as a contract for defining operations that can be executed on various processing engines,
    providing a consistent interface for different implementations.

    Attributes:
    - kwargs (dict): Additional keyword arguments specific to the operation.


    Usage:
    ```
    # Example of creating a custom operation
    class CustomOperation(Operation):
        def __init__(self, custom_parameter, **kwargs):
            super().__init__(**kwargs)
            self.custom_parameter = custom_parameter

        def apply(self, df):
            # Custom operation implementation using  self.kwargs, and self.custom_parameter
            result = df  # Replace this with the actual implementation
            return result

    # Example usage
    custom_operation = CustomOperation(spark, custom_parameter_value, additional_parameter=...)
    result_df = custom_operation.apply(input_df)
    ```
    """

    def __init__(self, **kwargs):
        """
        Initialize the Operation with parameters specific to the operation.

        Parameters:
        - kwargs (dict): Additional keyword arguments specific to the operation.
        """
        self.kwargs = kwargs

    @abstractmethod
    def apply(self, *df: Any) -> Any:
        """
        Abstract method to apply the operation on a given data frame.

         Parameters:
        - *dfs (Any): Variable number of input data frames on which the operation will be applied.

        Returns:
        - Any: The result of applying the operation on the input data frame(s).
        """
        pass
