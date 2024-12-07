import inspect
import json
import os
from datetime import datetime
from enum import Enum
from itertools import tee
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Literal,
    Optional,
    Sequence,
    Union,
    get_args,
    get_origin,
)

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator
from pyspark.sql.dataframe import DataFrame

CURRENT_FILE_DIR = os.path.dirname(os.path.abspath(__file__))


DATE_FORMATTER = {
    "year": lambda x: str(x.year),
    "month": lambda x: str(x.month).zfill(2),
    "day": lambda x: str(x.day).zfill(2),
}


class BucketEnvInheritException(Exception):
    """
    Exception raised when the environment is set to 'inherit'.
    """

    def __init__(self):
        self.message = (
            "Environment Env.INHERIT (the default value) was found in the input data for the bucket parameters. "
            "Please provide a valid environment in the bucket parameters."
        )
        super().__init__(self.message)


class PlaceholderDetectedException(Exception):
    """
    Exception raised when a placeholder is detected in the input data.
    """

    def __init__(self):
        self.message = (
            "Placeholder '{{processing_date}}' found in read_dates. "
            "Either provide a valid date, or use the 'inject_processing_date_into_dataframe_step_params' function to replace the placeholders in the StepParams object."
        )
        super().__init__(self.message)


class ReadPreviousDayException(Exception):
    """
    Exception raised when the dataframe from the previous day is not found.
    """

    def __init__(self, message: str = "Dataframe from the previous day not found"):
        self.message = message
        super().__init__(self.message)


class EmptyDataFrameException(Exception):
    """
    Exception raised when the dataframe is empty.
    """

    def __init__(self, message: str = "Dataframe is empty"):
        self.message = message
        super().__init__(self.message)


class HadoopS3FileSystem(str, Enum):
    """
    Enumeration representing different Hadoop file systems.

    Attributes:
        s3 (str): To be used inside EMR. This is the file system that leverages EMRFS (EMR File System).
        s3a (str): To be used outside EMR. This is the file system maintained by the Apache Hadoop project, which is a way more efficient version of the s3 file system (except when using EMR).
    """

    S3 = "s3"
    S3A = "s3a"


class FileType(str, Enum):
    """
    Represents the type of file used in data pipelines.

    Attributes:
        CSV (str): Represents a CSV file.
        JSON (str): Represents a JSON file.
        PARQUET (str): Represents a Parquet file.
        AVRO (str): Represents an AVRO file.
    """

    CSV = "csv"
    JSON = "json"
    PARQUET = "parquet"
    AVRO = "avro"


class S3Layer(str, Enum):
    """
    Enum class representing different layers in a data pipeline.

    The available layers are:
    - LANDING: The landing layer where raw data is initially ingested.
    - RAW: The raw layer where the ingested data is stored without any transformations.
    - TRUSTED: The trusted layer where the data is cleaned and validated.
    - ANALYTICS: The analytics layer where the data is transformed and aggregated for analysis.
    - GOLD: The gold layer where the data is stored for business intelligence.
    - DIAMOND: The diamond layer where the data is stored for machine learning.
    - SANDBOX: The sandbox layer where the data is stored for testing and experimentation.

    """

    LANDING = "landing"
    RAW = "raw"
    TRUSTED = "trusted"
    ANALYTICS = "analytics"
    GOLD = "gold"
    DIAMOND = "diamond"
    SANDBOX = "sandbox"


class Env(str, Enum):
    """
    Enumeration representing different environments.

    Attributes:
        DEV (str): Development environment.
        PRD (str): Production environment.
        STG (str): Staging environment.
        INHERIT (str): Placeholder that will be replaced with an actual environment, which is passed during the StepParams initialization.
    """

    DEV = "dev"
    PRD = "prd"
    STG = "stg"
    INHERIT = "inherit"


class DatePartition(str, Enum):
    """
    Enum representing different types of date partitions.

    Attributes:
        YEAR (str): Represents a partition by year, with name "year".
        MONTH (str): Represents a partition by month, with name "month".
        DAY (str): Represents a partition by day, with name "day".
    """

    YEAR = "year"
    MONTH = "month"
    DAY = "day"


class FnKind(str, Enum):
    """
    Enumeration representing the kind of function.

    Attributes:
        SINGLE (str): Represents a single function.
        BATCH (str): Represents a batch function.
    """

    SINGLE = "single"
    BATCH = "batch"


class SparkConfigParams(BaseModel):
    """
    Configuration parameters for Spark. Most relevant parameters are included as attributes for convenience, but additional configurations can be passed as a dictionary to the 'additional_configs' attribute. Omitting an attribute will make it use the default value.

    Attributes:
        spark_master (str): The URL of the Spark master.
        spark_executor_memory (str): The amount of memory to be allocated per executor.
        spark_driver_memory (str): The amount of memory to be allocated for the driver.
        spark_executor_memoryOverhead (str): The amount of off-heap memory to be allocated per executor.
        spark_driver_memoryOverhead (str): The amount of off-heap memory to be allocated for the driver.
        spark_task_maxFailures (str): The maximum number of task failures allowed per stage.
        spark_stage_maxConsecutiveAttempts (str): The maximum number of consecutive attempts allowed per stage.
        spark_sql_repl_eagerEval_enabled (str): Whether to enable eager evaluation in the Spark SQL REPL.
        spark_dynamicAllocation_enabled (str): Whether to enable dynamic allocation of executors.
        spark_log_level (str): The log level for Spark.
        additional_configs (Optional[Dict[str, str]]): Additional Spark configuration parameters.
    """

    model_config = ConfigDict(populate_by_name=True)

    spark_master: str = Field(default=None, alias=str(str("spark.master")))
    spark_executor_memory: str = Field(default=None, alias=str("spark.executor.memory"))
    spark_driver_memory: str = Field(default=None, alias=str("spark.driver.memory"))
    spark_executor_memoryOverhead: str = Field(
        default=None, alias=str("spark.executor.memoryOverhead")
    )
    spark_driver_memoryOverhead: str = Field(
        default=None, alias=str("spark.driver.memoryOverhead")
    )
    spark_task_maxFailures: str = Field(
        default=None, alias=str("spark.task.maxFailures")
    )
    spark_stage_maxConsecutiveAttempts: str = Field(
        default=None, alias=str("spark.stage.maxConsecutiveAttempts")
    )
    spark_dynamicAllocation_enabled: str = Field(
        default=None, alias=str("spark.dynamicAllocation.enabled")
    )
    spark_sql_repl_eagerEval_enabled: str = Field(
        default="true", alias=str("spark.sql.repl.eagerEval.enabled")
    )
    spark_log_level: str = Field(default="ERROR", alias=str("spark.log.level"))

    additional_configs: Optional[Dict[str, str]] = None


class BaseModelJsonDumps(BaseModel):
    """A base model class that extends Pydantic's BaseModel by overriding the __str__ to pretty print the model as JSON."""

    def __str__(self):
        return json.dumps(self.model_dump(), indent=2, default=str)


class AWSCredentials(BaseModelJsonDumps):
    """
    Represents AWS credentials required for authentication.

    Attributes:
        aws_access_key_id (str): The AWS access key ID.
        aws_secret_access_key (str): The AWS secret access key.
    """

    aws_access_key_id: str
    aws_secret_access_key: str


class S3BucketParams(BaseModelJsonDumps):
    """
    Represents the parameters for an S3 bucket, most specially the bucket name.

    Attributes:
        env (Env): The environment. Must be one of "Env.DEV" or "Env.PRD".
        s3_layer (Optional[S3Layer]): The s3 layer (optional).
        ng_prefix (str): The NG prefix. Defaults to "ng".
        bucket_name (Optional[str]): The bucket name (optional). If not provided, it will be generated based on the s3 layer, environment, and NG prefix.
    """

    env: Env
    s3_layer: Optional[S3Layer] = None
    ng_prefix: str = "ng"
    bucket_name: Optional[str] = None

    @model_validator(mode="before")
    def perform_adjustments(cls, data):
        env = data.get("env").value if data.get("env") is not None else None
        s3_layer = (
            data.get("s3_layer").value if data.get("s3_layer") is not None else None
        )
        ng_prefix = data.get("ng_prefix", "ng")
        bucket_name = data.get("bucket_name")

        if bucket_name is None:
            if s3_layer is None:
                raise ValueError(
                    "'s3_layer' must be provided if 'bucket_name' is not provided"
                )

            if env and env != Env.INHERIT:
                data["bucket_name"] = f"{ng_prefix}-datalake-{s3_layer}-{env}"

        return data


class S3ReadSchemaParams(BaseModelJsonDumps):
    """
    Represents the parameters for reading a schema from an S3 bucket.

    Attributes:
        bucket_params (S3BucketParams): The parameters for the S3 bucket.
        path (str): The path to the schema file in the S3 bucket.

    Methods:
        strip_slashes(v: str) -> str: A class method that strips leading and trailing slashes from the path.
        ensure_path_to_file_has_json_extension(v: str) -> str: A class method that ensures the path has a '.json' extension.
    """

    bucket_params: S3BucketParams
    path: str

    @field_validator("path")
    @classmethod
    def strip_slashes(cls, v: str) -> str:
        return v.strip("/")

    @field_validator("path")
    @classmethod
    def ensure_path_to_file_has_json_extension(cls, v: str) -> str:
        if not v.endswith(".json"):
            raise ValueError(
                f"For S3 schema, 'path' must have a '.json' extension. Received path: '{v}'"
            )

        return v


class DataFrameBaseParams(BaseModelJsonDumps):
    """
    Represents the base parameters for a DataFrame.

    Attributes:
        dataframe_bucket_params (S3BucketParams): The bucket parameters for the DataFrame.
        dataframe_specific_paths (Optional[Union[List[str], str]]): The specific path for the DataFrame. Defaults to None.
        dataframe_base_path (Optional[str]): The base path for the DataFrame. Defaults to None.
        dataframe_file_type (FileType): The file type of the DataFrame.
    """

    dataframe_bucket_params: S3BucketParams
    dataframe_base_path: Optional[str] = None
    dataframe_file_type: FileType

    @field_validator("dataframe_base_path")
    def strip_and_ensure_dataframe_base_path_parent_folder(cls, v: str) -> str:
        if v is not None:
            v = v.strip("/")

        if "/" not in v:
            raise ValueError(
                f"'dataframe_base_path' should have at least one parent folder inside the bucket. Ensure there is at least one slash ('/') in the path. Received path: '{v}'"
            )

        return v


class ReadDateParams(BaseModelJsonDumps):
    """
    Represents the parameters for reading dates in a data pipeline.

    Attributes:
        read_dates (Union[Sequence[Union[Union[str, datetime], List[Union[str, datetime]]]], datetime, Literal["{{processing_date}}"]]):
            The dates to be read. It can be a sequence of dates, a single date, or the literal "{{processing_date}}".
        processing_date_offset_days (Optional[int]):
            The number of days to offset the processing date. Defaults to None.
        date_partitions (dict[DatePartition, str]):
            A dictionary mapping date partitions to their corresponding names.
            Defaults to {DatePartition.YEAR: "year", DatePartition.MONTH: "month", DatePartition.DAY: "day"}.
        do_not_include_date_columns (bool):
            Indicates whether to exclude date columns when reading the DataFrame. Defaults to False. This means the default behavior is to include date columns coming from the date partitions.
        retry_look_window_days (int):
            The number of days to look back for retries. Must be between 0 and 30. Defaults to 0.
    """

    read_dates: Union[
        Sequence[Union[Union[str, datetime], List[Union[str, datetime]]]],
        datetime,
        Literal["{{processing_date}}"],
    ]
    processing_date_offset_days: Optional[int] = None
    was_offset_applied: bool = False
    date_partitions: dict[DatePartition, str] = {
        DatePartition.YEAR: "year",
        DatePartition.MONTH: "month",
        DatePartition.DAY: "day",
    }
    do_not_include_date_columns: bool = False
    retry_look_window_days: int = 0

    @model_validator(mode="before")
    def validate_offset_and_read_dates(cls, data):
        read_dates = data.get("read_dates")
        processing_date_offset_days = data.get("processing_date_offset_days")

        if processing_date_offset_days is not None:
            if read_dates != "{{processing_date}}":
                raise ValueError(
                    "If 'processing_date_offset_days' is provided, 'read_dates' must be '{{processing_date}}'"
                )

        return data

    @field_validator("retry_look_window_days")
    def ensure_retry_look_window_days_range(cls, v: int) -> int:
        if not 0 <= v <= 30:
            raise ValueError("'retry_look_window_days' must be between 0 and 30")

        return v

    @field_validator("date_partitions")
    def ensure_all_date_partitions(
        cls, v: dict[DatePartition, str]
    ) -> dict[DatePartition, str]:
        """
        Ensures that all date partitions are present in the input dictionary.

        Args:
            v (dict[DatePartition, str]): The input dictionary.

        Returns:
            dict[DatePartition, str]: The input dictionary.

        Raises:
            ValueError: If any date partition is missing.
        """
        date_partitions = [DatePartition.YEAR, DatePartition.MONTH, DatePartition.DAY]

        for date_partition in date_partitions:
            if date_partition not in v:
                raise ValueError(
                    f"Missing date partition: '{date_partition}'. The dictionary must contain all date partitions: {date_partitions}"
                )

        return v


class InputDataFrameParams(DataFrameBaseParams):
    """
    Parameters for input data frames.

    Attributes:
        pyspark_schema_struct (Optional[Dict[str, Any]]): The schema of the input data frame in PySpark StructType format.
        s3_schema_path_params (Optional[S3ReadSchemaParams]): The parameters for reading the schema from an S3 path.
        read_date_params (Optional[ReadDateParams]): The parameters for reading the date from the input data frame.
        dataframe_specific_paths (Optional[Union[List[str], str]]): The specific paths for the input data frame.
        allow_empty_dataframe (bool): Flag indicating whether an empty data frame is allowed.

    Methods:
        check_schema_mode(cls, data): Check the schema mode and validate the input data.
        xor_specific_path_and_dataframe_base_path(cls, data): Validate that specific paths and base path are not passed together.
        xor_specific_path_and_read_date_params(cls, data): Validate that specific paths and read date params are not passed together.
        strip_dataframe_specific_paths(cls, v: str) -> str: Strip leading and trailing slashes from the specific paths.

    Raises:
        ValueError: If 'pyspark_schema_struct' and 's3_schema_path_params' are passed together.
        ValueError: If 'dataframe_specific_paths' and 'dataframe_base_path' are passed together.
        ValueError: If neither 'dataframe_specific_paths' nor 'dataframe_base_path' are passed.
        ValueError: If 'dataframe_specific_paths' and 'read_date_params' are passed together.
    """

    dataframe_specific_paths: Optional[Union[List[str], str]] = None
    pyspark_schema_struct: Optional[Dict[str, Any]] = None
    s3_schema_path_params: Optional[S3ReadSchemaParams] = None
    read_date_params: Optional[ReadDateParams] = None
    allow_empty_dataframe: bool = False

    @model_validator(mode="before")
    def check_schema_mode(cls, data):
        """
        Check the schema mode and validate the input data.

        Args:
            cls: The class object.
            data: The input data dictionary.

        Returns:
            The validated input data dictionary.

        Raises:
            ValueError: If 'pyspark_schema_struct' and 's3_schema_path_params' are passed together.
        """
        pyspark_schema_struct = data.get("pyspark_schema_struct")
        s3_schema_path_params = data.get("s3_schema_path_params")

        if pyspark_schema_struct is not None and s3_schema_path_params is not None:
            raise ValueError(
                "'pyspark_schema_struct' and 's3_schema_path_params' cannot be passed together"
            )

        return data

    @model_validator(mode="before")
    def xor_specific_path_and_dataframe_base_path(cls, data):
        """
        Validate that specific paths and base path are not passed together.

        Args:
            cls: The class object.
            data: The input data dictionary.

        Returns:
            The validated input data dictionary.

        Raises:
            ValueError: If 'dataframe_specific_paths' and 'dataframe_base_path' are passed together.
            ValueError: If neither 'dataframe_specific_paths' nor 'dataframe_base_path' are passed.
        """
        dataframe_specific_paths = data.get("dataframe_specific_paths")
        dataframe_base_path = data.get("dataframe_base_path")

        if dataframe_specific_paths is not None and dataframe_base_path is not None:
            raise ValueError(
                "'dataframe_specific_paths' and 'dataframe_base_path' cannot be passed together"
            )

        if dataframe_specific_paths is None and dataframe_base_path is None:
            raise ValueError(
                "Either 'dataframe_specific_paths' or 'dataframe_base_path' should be passed"
            )

        return data

    @model_validator(mode="before")
    def xor_specific_path_and_read_date_params(cls, data):
        """
        Validate that specific paths and read date params are not passed together.

        Args:
            cls: The class object.
            data: The input data dictionary.

        Returns:
            The validated input data dictionary.

        Raises:
            ValueError: If 'dataframe_specific_paths' and 'read_date_params' are passed together.
        """
        dataframe_specific_paths = data.get("dataframe_specific_paths")
        read_date_params = data.get("read_date_params")

        if dataframe_specific_paths is not None and read_date_params is not None:
            raise ValueError(
                "'dataframe_specific_paths' and 'read_date_params' cannot be passed together"
            )

        return data

    @field_validator("dataframe_specific_paths")
    def strip_dataframe_specific_paths(cls, v: str) -> str:
        """
        Strip leading and trailing slashes from the specific paths.

        Args:
            cls: The class object.
            v: The specific paths.

        Returns:
            The stripped specific paths.
        """
        if v is not None:
            if isinstance(v, list):
                return [x.strip("/") for x in v]  # type: ignore
            else:
                return v.strip("/")


class SingleWriteDateParams(BaseModelJsonDumps):
    """
    Represents the parameters for a single write date.

    Attributes:
        single_write_date (Union[datetime, Literal["{{processing_date}}"]]):
            The single write date. It can be either a datetime object or the string "{{processing_date}}".
        single_write_date_partitions (List[str]):
            The list of partitions to be used for the single write date. Defaults to ["year", "month", "day"].
    """

    single_write_date: Union[datetime, Literal["{{processing_date}}"]]
    single_write_date_partitions: dict[DatePartition, str] = {
        DatePartition.YEAR: "year",
        DatePartition.MONTH: "month",
        DatePartition.DAY: "day",
    }

    @field_validator("single_write_date_partitions")
    def ensure_all_date_partitions(
        cls, v: dict[DatePartition, str]
    ) -> dict[DatePartition, str]:
        """
        Ensures that all date partitions are present in the input dictionary.

        Args:
            v (dict[DatePartition, str]): The input dictionary.

        Returns:
            dict[DatePartition, str]: The input dictionary.

        Raises:
            ValueError: If any date partition is missing.
        """
        date_partitions = [DatePartition.YEAR, DatePartition.MONTH, DatePartition.DAY]

        for date_partition in date_partitions:
            if date_partition not in v:
                raise ValueError(
                    f"Missing date partition: '{date_partition}'. The dictionary must contain all date partitions: {date_partitions}"
                )

        return v


class OutputDataFrameParams(DataFrameBaseParams):
    """
    Parameters for writing output dataframes.

    Attributes:
        dataframe_specific_path (Optional[str]): The specific path for the dataframe.
        write_schema_on_s3 (bool): Whether to write the schema on S3.
        overwrite (bool): Whether to overwrite existing data.
        single_write_date_params (Optional[SingleWriteDateParams]): Parameters for single write date.
        partition_by (Optional[List[str]]): List of columns to partition the data by.
        coalesce_amount (Optional[int]): The number of partitions to coalesce the DataFrame into before writing.
        repartition_amout (Optional[int]): The number of partitions to repartition the DataFrame into before writing.
    """

    dataframe_specific_path: Optional[str] = None
    write_schema_on_s3: bool = True
    overwrite: bool = False
    single_write_date_params: Optional[SingleWriteDateParams] = None
    partition_by: Optional[List[str]] = None
    coalesce_amount: Optional[int] = None
    repartition_amout: Optional[int] = None

    @model_validator(mode="before")
    def xor_specific_path_and_dataframe_base_path(cls, data):
        dataframe_specific_path = data.get("dataframe_specific_path")
        dataframe_base_path = data.get("dataframe_base_path")

        if dataframe_specific_path is not None and dataframe_base_path is not None:
            raise ValueError(
                "'dataframe_specific_path' and 'dataframe_base_path' cannot be passed together"
            )

        if dataframe_specific_path is None and dataframe_base_path is None:
            raise ValueError(
                "Either 'dataframe_specific_path' or 'dataframe_base_path' should be passed"
            )

        return data

    @model_validator(mode="before")
    def ensure_date_partitions_in_partition_by(cls, data):
        def is_sublist(smaller, larger):
            if not smaller:
                return True
            if not larger:
                return False

            it = iter(larger)
            smaller_it = tee(smaller, 1)[0]

            return any(
                all(x == y for x, y in zip(smaller_it, it))
                for _ in range(len(larger) - len(smaller) + 1)
            )

        single_write_date_params = data.get("single_write_date_params")
        partition_by = data.get("partition_by")

        if single_write_date_params is None:
            return data

        if partition_by is None:
            raise ValueError(
                "'partition_by' must be provided when using 'single_write_date_params', with at least the date partitions provided in 'single_write_date_params.single_write_date_partitions'."
            )

        if not is_sublist(
            single_write_date_params.single_write_date_partitions.values(), partition_by
        ):
            raise ValueError(
                "Date partitions in 'single_write_date_params.single_write_date_partitions' must be a subset (respecting the order) of 'partition_by'."
            )

        return data

    @field_validator("partition_by")
    def ensure_unique_partition_by(cls, v: List[str]) -> List[str]:
        if len(v) != len(set(v)):
            raise ValueError("'partition_by' must contain unique columns")
        return v


class FnIndirect(BaseModelJsonDumps):
    fn_name: str
    fn_path: str


class DataFrameTransformParams(BaseModelJsonDumps):
    """
    Represents the parameters for a data transformation function.

    Attributes:
        transform_function (Callable): The transformation function to be applied.
        transform_description (str): A description of the transformation function.
        fn_kwargs (Optional[dict]): Optional keyword arguments for the transformation function.
        force_extract_partitions (Optional[List[int]]): Optional list of partitions to force extract.
    """

    transform_function: Callable
    transform_description: str
    fn_kwargs: Optional[dict] = None
    force_extract_partitions: Optional[List[int]] = None

    @model_validator(mode="before")
    def validate_transform_function_signature(cls, data):
        transform_function = data.get("transform_function")

        def is_annotation_dict_dataframe(annotation):
            origin = get_origin(annotation)
            args = get_args(annotation)

            if origin is dict and args[0] is str and issubclass(args[1], DataFrame):
                return True

            return False

        signature = inspect.signature(transform_function)
        parameters = signature.parameters
        first_param_annotation = (
            list(parameters.values())[0].annotation if parameters else None
        )
        return_annotation = signature.return_annotation

        if not is_annotation_dict_dataframe(first_param_annotation):
            raise ValueError(
                f"Function must have 'dict[str, DataFrame]' as first parameter hint. Received: '{first_param_annotation}'\nValid function signature example: def transform_fn(dfs: dict[str, DataFrame]) -> dict[str, DataFrame]: ..."
            )

        if not is_annotation_dict_dataframe(return_annotation):
            raise ValueError(
                f"Function must have 'dict[str, DataFrame]' as return type hint. Received: '{return_annotation}'.\nValid function signature example: def transform_fn(dfs: dict[str, DataFrame]) -> dict[str, DataFrame]: ..."
            )

        return data


DataFrameDict = Dict[str, DataFrame]
InputDataFrameParamsDict = Dict[str, InputDataFrameParams]
OutputDataFrameParamsDict = Dict[str, OutputDataFrameParams]


class DataFrameStepParams(BaseModelJsonDumps):
    """
    Represents the parameters for a step in a data pipeline.

    Attributes:
        default_env (Env): The default environment if the environment is not provided in the dataframe bucket parameters. Cannot be "Env.INHERIT".
        input_dataframes_params (InputDataFrameParamsDict): The parameters for input dataframes.
        transform_params (Optional[TransformParams]): The parameters for the transform step. Defaults to None.
        output_dataframes_params (Optional[OutputDataFrameParamsDict]): The parameters for output dataframes. Defaults to None.
    """

    default_env: Env
    input_dataframes_params: InputDataFrameParamsDict
    transform_params: Optional[DataFrameTransformParams] = None
    output_dataframes_params: Optional[OutputDataFrameParamsDict] = None
    trusted_prev_day_env: Env = Env.INHERIT

    @field_validator("default_env")
    def check_not_inherit(cls, v: Env):
        if v == Env.INHERIT:
            valid_envs = [e.value for e in Env if e != Env.INHERIT]
            raise ValueError(
                f"INHERIT is not allowed for default_env. Please choose between {valid_envs}"
            )
        return v

    def __init__(self, **data):
        super().__init__(**data)
        self.set_env_and_bucket_name_all_dataframes(self.input_dataframes_params)
        if self.output_dataframes_params:
            self.set_env_and_bucket_name_all_dataframes(self.output_dataframes_params)

    def set_env_and_bucket_name_all_dataframes(self, dataframe_params_dict):
        for dataframe_params in dataframe_params_dict.values():
            if isinstance(dataframe_params, InputDataFrameParams):
                processing_date_offset_days = (
                    dataframe_params.read_date_params.processing_date_offset_days
                    if dataframe_params.read_date_params
                    else None
                )
                self.set_env_and_bucket_name(
                    bucket_params=dataframe_params.dataframe_bucket_params,
                    processing_date_offset_days=processing_date_offset_days,
                )
                if dataframe_params.s3_schema_path_params:
                    self.set_env_and_bucket_name(
                        bucket_params=dataframe_params.s3_schema_path_params.bucket_params,
                    )
            else:
                self.set_env_and_bucket_name(
                    bucket_params=dataframe_params.dataframe_bucket_params
                )

    def set_env_and_bucket_name(
        self,
        bucket_params: S3BucketParams,
        processing_date_offset_days: Optional[int] = None,
    ):
        if (
            bucket_params.s3_layer == S3Layer.TRUSTED
            and processing_date_offset_days == -1
        ):
            bucket_params.env = self.trusted_prev_day_env
        if bucket_params.env == Env.INHERIT:
            bucket_params.env = self.default_env
        if not bucket_params.bucket_name:
            assert bucket_params.s3_layer is not None
            bucket_params.bucket_name = f"{bucket_params.ng_prefix}-datalake-{bucket_params.s3_layer.value}-{bucket_params.env.value}"


DataFrameStepParamsDict = Dict[str, DataFrameStepParams]


class CustomStepParams(BaseModelJsonDumps):
    params: Optional[Dict[str, Any]] = None
