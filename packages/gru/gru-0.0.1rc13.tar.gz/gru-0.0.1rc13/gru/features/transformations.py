from pydantic import BaseModel, validator
from typing import Dict, Any

class BuiltInTransformation(BaseModel):
    """
    Pydantic model for validating built-in Spark transformations configurations.

    This model validates configurations for Spark's built-in transformations like
    filter, selectExpr, and repartition.

    Attributes:
        type (str): Type of built-in transformation ('filter', 'selectExpr', 'repartition')
        additional_params (Dict[str, Any]): Parameters required for the transformation

    Examples:
        >>> # Valid filter transformation
        >>> config = BuiltInTransformation(
        ...     type="filter",
        ...     additional_params={"condition": "col('age') > 18"}
        ... )

        >>> # Valid selectExpr transformation
        >>> config = BuiltInTransformation(
        ...     type="selectExpr",
        ...     additional_params={"expression": "upper(name) as uppercase_name"}
        ... )

        >>> # Invalid configuration (will raise ValueError)
        >>> config = BuiltInTransformation(
        ...     type="filter",
        ...     additional_params={}  # Missing required 'condition' parameter
        ... )
    """

    type: str
    additional_params: Dict[str, Any]

    @validator('additional_params')
    def validate_params(cls, v, values):
        type = values.get('type')
        required_params = {
            'filter': ['condition'],
            'selectExpr': ['expression'],
            'repartition': ['numPartitions'],
        }

        if type not in required_params:
            raise ValueError(f"Unsupported transformation type: {type}")

        for param in required_params[type]:
            if param not in v:
                raise ValueError(f"{type.capitalize()} transformation must have a '{param}' parameter")

        return v

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": self.type,
            "additional_params": self.additional_params
        }

class LambdaTransformation(BaseModel):
    """
    Pydantic model for validating Lambda UDF (User Defined Function) transformations.

    This model validates configurations for map and flatMap transformations that use
    lambda functions as UDFs in Spark.

    Attributes:
        type (str): Type of transformation ('map' or 'flatMap')
        function (str): Lambda function as string

    Examples:
        >>> # Valid map transformation
        >>> config = LambdaTransformation(
        ...     type="map",
        ...     function="lambda x: x * 2"
        ... )

        >>> # Valid flatMap transformation
        >>> config = LambdaTransformation(
        ...     type="flatMap",
        ...     function="lambda text: text.split()"
        ... )

        >>> # Invalid function (will raise ValueError)
        >>> config = LambdaTransformation(
        ...     type="map",
        ...     function="def multiply(x): return x * 2"  # Not a lambda function
        ... )
    """

    type: str
    function: str

    @validator('type')
    def validate_type(cls, v):
        allowed_types = ['map', 'flatMap']
        if v not in allowed_types:
            raise ValueError(f"Unsupported transformation type: {v}. Allowed types are {allowed_types}")
        return v

    @validator('function')
    def validate_function(cls, v, values):
        type = values.get('type')
        if not v.startswith('lambda'):
            raise ValueError(f"Function must be a lambda expression")

        # Split the lambda function to get parameters
        params = v.split(':')[0].strip().lstrip('lambda').strip().split(',')

        if type == 'map':
            if len(params) < 1:
                raise ValueError("Map function must have at least one parameter")
        elif type == 'flatMap':
            if len(params) < 1:
                raise ValueError("FlatMap function must have at least one parameter")
        return v

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": self.type,
            "function": self.function,
        }
