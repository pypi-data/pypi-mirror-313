"""
Data Sources are an abstraction on top of datasets that enable

 - A standardized way of declaring raw data on top of which features & pre-processing tables are calculated
 - A simplified experience while referencing in defining features - Data Scientists can focus on the feature logic without having to worry about the underlying data, DB connections, accesses etc.
 - Reusability while defining and materializing features/pre-processing transforms
 - Improved understanding of raw data

Functions: 
    - return_col_details
    - return_schema
    - check_argument_type
    - register_datasource
"""
from abc import abstractmethod
from datetime import datetime
import json
from typing import Any, Dict, List, Optional, Union

from gru.schema.registrable import Registrable
from gru.sources.file_types import CSVType, ParquetType
from gru.utils.data_types import DataType
from gru.utils.entity_type import EntityType


class Column:
    """
    Define the column of data source

    Parameters
    ----------
    self:
        python self object
    name:
        name of the column
    type:
        data type of the column
    nullable:
        If set to True, then the column can have Null value. If False, then the column can't be Null
    description:
        Description of the column

    Notes
    -----

    Examples
    --------
    >>> schema_obj = Schema(
    ...     user_schema=[
    ...         Column("user_id", DataTypes.STRING, True, "Unique User Identifier"),
    ...         Column("offer_id", DataTypes.STRING, True, "Offer viewed by the User"),
    ...         Column("clicked_at", DataTypes.TIMESTAMP, True, "Time of offer click"),
    ...         Column("viewed_at", DataTypes.STRING, True, "Time of Offer View"),
    ...         Column(
    ...             "view_to_click_time_mins", DataTypes.FLOAT, True, "View to Click time in minutes"
    ...         ),
    ...     ]
    ... )
    """

    def __init__(self, name, type: DataType, nullable=True, description=""):
        """
        :param name: Name of the column
        :param type: Datatype of the column
        :param nullable: Nullable or not
        :param description: Description of the column
        """
        self.name = name
        self.type = type.value
        self.nullable = nullable
        self.description = description
        self.col_details = [self.name, self.type, self.nullable, self.description]
        self.return_col_details()

    def return_col_details(self):
        return self.col_details


class Schema:
    """
    Define the schema of the data source

    Parameters
    ----------
    self:
        python self object
    user_schema: List[Column]
        user_schema is the list of columns present in the datasource.

    Notes
    -----

    Examples
    --------
    >>> schema_obj = Schema(
    ...     user_schema=[
    ...         Column("user_id", DataTypes.STRING, True, "Unique User Identifier"),
    ...         Column("offer_id", DataTypes.STRING, True, "Offer viewed by the User"),
    ...         Column("clicked_at", DataTypes.TIMESTAMP, True, "Time of offer click"),
    ...         Column("viewed_at", DataTypes.STRING, True, "Time of Offer View"),
    ...         Column(
    ...             "view_to_click_time_mins", DataTypes.FLOAT, True, "View to Click time in minutes"
    ...         ),
    ...     ]
    ... )
    """

    def __init__(self, user_schema: List[Column]):
        self.user_schema = user_schema

        self.pyspark_schema = self.convert_to_pyspark_schema()
        self.bq_schema = self.convert_to_bq_schema()

        self.return_schema(self.pyspark_schema, self.bq_schema)

    def convert_to_pyspark_schema(self):
        """Method to convert column details list to pyspark like schema and append to the schema dictionary"""
        self.schema = {}
        col_schema = []
        for column_obj in self.user_schema:
            col = column_obj.col_details
            col_schema.append(
                {
                    "metadata": {},
                    "name": col[0],
                    "nullable": col[2],
                    "type": col[1],
                }
            )
        self.schema = {"fields": col_schema, "type": "struct"}
        return self.schema

    def convert_to_bq_schema(self):
        """Method to convert column details list to BQ like schema and append to the schema dictionary"""
        self.schema = []
        for column_obj in self.user_schema:
            col = column_obj.col_details
            self.schema.append(
                {
                    "name": col[0],
                    "nullable": col[2],
                    "type": col[1],
                    "description": col[3],
                }
            )
        return self.schema

    def return_schema(self, pyspark_schema, bq_schema):
        self.schema = {
            "pyspark_schema": pyspark_schema,
            "bq_schema": bq_schema,
        }
        return str(self.schema)


class DataSource(Registrable):
    """
    A generic class for any data source that will act as the parent class for all the data sources to be supported in future.

    """

    def __init__(
        self,
        name: str,
        description: str,
        family: str,
        processing_paradigm: str,
        additional_read_configs: Optional[Dict[str, Any]] = {},
        cloud_provider: str = None,
        file_type: Union[CSVType, ParquetType] = None,
        physical_uri: Dict[str, Any] = None,
        schema: Schema = None,
        type: str = None,
        metadata: Optional[Dict[str, str]] = {},
        event_timestamp_field: str = None,
        event_timestamp_format: str = None,
        owners: Union[List[str], str] = [],
        created_at=datetime.now(),
    ):
        self.name = name
        self.family = family
        self.description = description
        self.processing_paradigm = processing_paradigm
        self.file_type = file_type
        self.entity_type = EntityType.DATA_SOURCE.value
        self.physical_uri = physical_uri
        self.additional_read_configs = additional_read_configs
        self.schema = schema
        self.type = type
        self.cloud_provider = cloud_provider
        self.metadata = metadata
        self.event_timestamp_field = event_timestamp_field
        self.event_timestamp_format = event_timestamp_format
        self.owners = owners
        self.created_at = created_at

    @abstractmethod
    def to_json(self) -> Dict:
        """
        Returns a json-formatted object representing this entity.
        """
        pass

    def __str__(self) -> str:
        return json.dumps(self.to_json(), indent=2, sort_keys=True)

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, other: object) -> bool:
        return isinstance(other, self.__class__) and self.to_json() == other.to_json()
    
    def to_register_json(self) -> Dict:
        return self.to_json()
