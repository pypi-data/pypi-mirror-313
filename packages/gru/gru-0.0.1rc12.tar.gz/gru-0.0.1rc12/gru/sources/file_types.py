"""
Specify FileTypes and other options that are necessary to load data from DataSources
"""
from typing import Optional


class CSVType:
    """
    Represents a CSV File/Object

    Parameters
    ----------
    #TODO - Defaults need to be corrected
    sep: Optional[str]
        delimiter; by default ','
    inferSchema: Optional[bool]
        by default set to False
    header: Optional[bool]
        if True, will read the first row of csv file as column names. by default set to False
    quotes: Optional[str]
        When you have a column with a delimiter in the data that is used to split the columns, use quotes option to specify the quote character, by default it is ” and delimiters inside quotes are ignored. Using this option you can set any quote character.
    nullValue: Optional[str]
        Using nullValue option you can specify the string in a CSV to consider as null. For example, if you want to set "manik" in name column to null
        |-- age: long (nullable = true) # 26
        |-- name: string (nullable = true) # manik
        +---+----+
        |age|name|
        +---+----+
        | 26|null|
        +---+----+
    nanValue: Optional[str]
        Using nanValue option you can specify the number in a CSV to consider as nan. For example, if you want to set 23.4 in name column to nan
    dateFormat: Optional[str]
        by default "yyyy-MM-dd HH:mm:ss"
    timestampFormat: Optional[str]
        by default "yyyy-MM-ddTHH:mm:ss.%f"
    encoding: Optional[str]
        by default set to 'utf-8' encoding

    Notes
    -----
    See Default values of Options - https://spark.apache.org/docs/latest/sql-data-sources-csv.html#data-source-option

    Examples
    --------
    >>> data_source_obj = S3DataSource(
    ...     data_source_name="my_data_source_11",
    ...     bucket="market-intelligence-platform",
    ...     base_key="sales/raw_data",
    ...     varying_key_suffix_format="d=%Y-%m-%d/h=%H%M",
    ...     varying_key_suffix_freq="15min",
    ...     time_offset=5*60,   
    ...     description="random desc of data source",
    ...     owners=["xyz"],
    ...     created_at=datetime(2022, 12, 20, 00, 00, 00),
    ...     file_type=CSVType(sep='|', header=True),
    ...     schema=schema_obj,
    ...     event_timestamp_field="viewed_at",
    ...     event_timestamp_format="%Y-%m-%d %H:%M",
    ... )
    """

    def __init__(
        self,
        sep: Optional[str] = None,
        inferSchema: Optional[bool] = None,
        header: Optional[bool] = None,
        quote: Optional[str] = None,
        nullValue: Optional[str] = None,
        nanValue: Optional[str] = None,
        dateFormat: Optional[str] = None,
        timestampFormat: Optional[str] = None,
        encoding: Optional[str] = None,
    ):
        """
        :param sep: delimiter; by default ','
        :param inferSchema: by default set to False
        :param header: if True, will read the first row of csv file as column names. by default set to False
        :param nullValue: Default `None`
        :param nanValue: Default `None`
        :param dateFormat: by default "yyyy-MM-dd HH:mm:ss"
        :param timestampFormat: by default "yyyy-MM-ddTHH:mm:ss.%f"
        :param encoding: Default `None`
        
        See Default values of Options in Spark - https://spark.apache.org/docs/latest/sql-data-sources-csv.html#data-source-option
        """

        self.sep = sep
        self.inferSchema = inferSchema
        self.header = header
        self.quote = quote
        self.nullValue = nullValue
        self.nanValue = nanValue
        self.dateFormat = dateFormat
        self.timestampFormat = timestampFormat
        self.encoding = encoding
        self.type = "CSV"

        self.options = {
            "type": self.type,
            "delimiter": self.sep,
            "inferSchema": self.inferSchema,
            "header": self.header,
            "quotes": self.quote,
            "nullValue": self.nullValue,
            "nanValue": self.nanValue,
            "dateFormat": self.dateFormat,
            "timestampFormat": self.timestampFormat,
            "encoding": self.encoding,
        }

        self.options = {k: v for k, v in self.options.items() if v is not None}


class ParquetType:
    """
    Represents a Parquet File/Object

    Parameters
    ----------
    mergeSchema: Optional[bool]
        if True, will merge schema of multiple parquet files while doing a Union, by default 'False'
    
    Notes
    -----

    Examples
    --------
    >>> data_source_obj = S3DataSource(
    ...     data_source_name="my_data_source_11",
    ...     bucket="market-intelligence-platform",
    ...     base_key="sales/raw_data",
    ...     varying_key_suffix_format="d=%Y-%m-%d/h=%H%M",
    ...     varying_key_suffix_freq="15min",
    ...     time_offset=5*60,   
    ...     description="random desc of data source",
    ...     owners=["xyz"],
    ...     created_at=datetime(2022, 12, 20, 00, 00, 00),
    ...     file_type=ParquetType(mergeSchema=True),
    ...     schema=schema_obj,
    ...     event_timestamp_field="viewed_at",
    ...     event_timestamp_format="%Y-%m-%d %H:%M",
    ... )
    """

    def __init__(self, mergeSchema: Optional[bool] = False):
        """
        :param mergeSchema: if True, will merge schema of multiple parquet files while doing a Union, by default 'False'
        """
        self.mergeSchema = mergeSchema
        self.type = "PARQUET"
        self.options = {"type": self.type, "mergeSchema": self.mergeSchema}
