import json
from datetime import datetime, timedelta
from typing import Annotated, Any, Dict, Optional, Union

from pyspark.sql import DataFrame
from pyspark.sql.functions import format_string, lit
from pyspark.sql.types import StructType

from ng_data_pipelines_sdk.aws_interface import AWSInterface
from ng_data_pipelines_sdk.custom_logger import logger
from ng_data_pipelines_sdk.interfaces import (
    DATE_FORMATTER,
    AWSCredentials,
    BucketEnvInheritException,
    DataFrameDict,
    DataFrameStepParams,
    DataFrameStepParamsDict,
    DataFrameTransformParams,
    DatePartition,
    EmptyDataFrameException,
    Env,
    FileType,
    HadoopS3FileSystem,
    InputDataFrameParams,
    InputDataFrameParamsDict,
    OutputDataFrameParams,
    OutputDataFrameParamsDict,
    PlaceholderDetectedException,
    S3BucketParams,
    S3Layer,
    S3ReadSchemaParams,
    SparkConfigParams,
)
from ng_data_pipelines_sdk.spark_manager import SparkManager
from ng_data_pipelines_sdk.utils import (
    generate_date_paths,
    handle_pyspark_timestamp_in_schema,
)

logger.setLevel("INFO")


class DataFrameManager:
    def __init__(
        self,
        hadoop_s3_file_system: HadoopS3FileSystem,
        spark_app_name: str = "spark_app",
        spark_config_params: SparkConfigParams = SparkConfigParams(),
        aws_credentials_dict: Optional[Dict[Env, AWSCredentials]] = None,
        aws_region_name: str = "us-east-1",
        log_level: str = "INFO",
        display_initial_message: bool = True,
    ):
        """
        Initializes the DataFrameManager.
        Args:
            hadoop_s3_file_system (HadoopS3FileSystem): The Hadoop S3 file system instance.
            spark_app_name (str, optional): The name of the Spark application. Defaults to "spark_app".
            spark_config_params (SparkConfigParams, optional): Configuration parameters for Spark. Defaults to SparkConfigParams().
            aws_credentials_dict (Optional[Dict[Env, AWSCredentials]], optional): AWS credentials dictionary. Defaults to None.
            aws_region_name (str, optional): The AWS region name. Defaults to "us-east-1".
            log_level (str, optional): The logging level. Defaults to "INFO".
            display_initial_message (bool, optional): Whether to display an initial message. Defaults to True.
        """
        self.hadoop_s3_file_system = hadoop_s3_file_system
        self.aws_interface = AWSInterface(
            region_name=aws_region_name,
            aws_credentials_dict=aws_credentials_dict,
        )
        self.spark_manager = SparkManager(
            app_name=spark_app_name,
            hadoop_s3_file_system=hadoop_s3_file_system,
            aws_credentials_dict=aws_credentials_dict,
            spark_config_params=spark_config_params,
        )
        self.completed_steps = []

        logger.setLevel(log_level)

        if display_initial_message:
            logger.info("DataFrameManager initialized.")

    def _get_bucket_url(self, bucket_params: S3BucketParams) -> str:
        return f"{self.hadoop_s3_file_system}://{bucket_params.bucket_name}"

    def convert_schema_object_to_pyspark_schema(
        self, schema_object: Dict[str, Any]
    ) -> StructType:
        logger.debug("Converting schema object to PySpark StructType...")
        pyspark_schema = StructType.fromJson(schema_object)
        pyspark_schema = handle_pyspark_timestamp_in_schema(pyspark_schema)
        logger.debug(f"Schema converted sucessfully: {pyspark_schema}")

        return pyspark_schema

    def retrieve_schema_from_s3(
        self, s3_read_schema_params: S3ReadSchemaParams
    ) -> StructType:
        """
        Retrieve the schema for the data from an AWS S3 bucket.

        Returns:
            pyspark.sql.types.StructType: The retrieved schema.

        Raises:
            ValueError: If there is an issue retrieving or handling the schema.
        """
        if s3_read_schema_params.bucket_params.bucket_name is None:
            raise ValueError("bucket_name must be provided")

        bucket_name = s3_read_schema_params.bucket_params.bucket_name
        path_to_file = s3_read_schema_params.path
        full_s3_file_path = (
            f"{self.hadoop_s3_file_system}://{bucket_name}/{path_to_file}"
        )

        logger.debug(f"Retrieving schema from path '{full_s3_file_path}'...")
        try:
            # Retrieve the schema object from AWS S3
            schema_object = self.aws_interface.get_object_aws(
                env=s3_read_schema_params.bucket_params.env,
                bucket_name=bucket_name,
                object_name=path_to_file,
            )

            # Decode the object to a string
            schema_str = schema_object.decode("utf-8").strip()

            # Convert the string to JSON
            schema_json = json.loads(schema_str)

            # Convert the JSON schema to a PySpark StructType
            pyspark_schema = StructType.fromJson(schema_json)

            logger.debug(f"Schema retrieved sucessfully: {pyspark_schema}")

            # Handle any timestamp issues in PySpark schema, if necessary
            return handle_pyspark_timestamp_in_schema(pyspark_schema)
        except Exception as e:
            error_message = (
                f"Error retrieving or handling schema from {full_s3_file_path}: {e}"
            )
            logger.error(error_message)
            raise ValueError(error_message)

    def read_dataframe(
        self,
        input_df_params: InputDataFrameParams,
        persist: bool = False,
        verbosity: Annotated[int, 0, 2] = 2,
        truncate: Union[int, bool] = False,
        print_schema: bool = False,
    ) -> DataFrame:
        """
        Reads a DataFrame from a specified location.

        Args:
            df_params (InputDataFrameParams): The parameters for reading the DataFrame.

        Returns:
            DataFrame: The read DataFrame.

        """
        bucket_url = self._get_bucket_url(input_df_params.dataframe_bucket_params)
        if input_df_params.dataframe_base_path:
            full_base_path = f"{bucket_url}/{input_df_params.dataframe_base_path}"
        else:
            full_base_path = None

        if input_df_params.dataframe_specific_paths:
            if isinstance(input_df_params.dataframe_specific_paths, list):
                paths = [
                    f"{bucket_url}/{path}"
                    for path in input_df_params.dataframe_specific_paths
                ]
            else:
                paths = f"{bucket_url}/{input_df_params.dataframe_specific_paths}"
        elif input_df_params.read_date_params:
            if input_df_params.read_date_params.read_dates == "{{processing_date}}":
                raise PlaceholderDetectedException()

            date_partitions = input_df_params.read_date_params.date_partitions
            paths = generate_date_paths(
                base_path=f"{bucket_url}/{input_df_params.dataframe_base_path}",
                dates=input_df_params.read_date_params.read_dates,
                year_partition=date_partitions.get(DatePartition.YEAR, "year"),
                month_partition=date_partitions.get(DatePartition.MONTH, "month"),
                day_partition=date_partitions.get(DatePartition.DAY, "day"),
            )

            # Prevent pyspark from adding date columns to the DataFrame
            if input_df_params.read_date_params.do_not_include_date_columns:
                full_base_path = None
        else:
            paths = f"{bucket_url}/{input_df_params.dataframe_base_path}"

        if input_df_params.pyspark_schema_struct:
            schema = self.convert_schema_object_to_pyspark_schema(
                schema_object=input_df_params.pyspark_schema_struct
            )
        elif input_df_params.s3_schema_path_params:
            schema = self.retrieve_schema_from_s3(input_df_params.s3_schema_path_params)
        else:
            schema = None

        if verbosity >= 2:
            logger.info("Starting read operation.")

        df = self.spark_manager.read(
            env=input_df_params.dataframe_bucket_params.env,
            paths=paths,
            file_type=input_df_params.dataframe_file_type,
            base_path=full_base_path,
            schema=schema,
            persist=persist,
        )

        if verbosity >= 2:
            logger.info("Read operation completed successfully.")

        if df is None:
            raise EmptyDataFrameException
        else:
            # Convert date partitions to string and add leading zeros because PySpark reads them as integers
            if input_df_params.read_date_params and full_base_path:
                date_partitions = input_df_params.read_date_params.date_partitions
                year_col_name = date_partitions.get(DatePartition.YEAR, "year")
                month_col_name = date_partitions.get(DatePartition.MONTH, "month")
                day_col_name = date_partitions.get(DatePartition.DAY, "day")

                df = (
                    df.withColumn(
                        year_col_name,
                        format_string("%04d", df[year_col_name]),
                    )
                    .withColumn(
                        month_col_name,
                        format_string("%02d", df[month_col_name]),
                    )
                    .withColumn(
                        day_col_name,
                        format_string("%02d", df[day_col_name]),
                    )
                )

        if verbosity >= 1:
            df.show(1, truncate=truncate)

        if print_schema:
            print("Schema:")
            df.printSchema()

        return df

    def write_schema(
        self, df: DataFrame, output_df_params: OutputDataFrameParams
    ) -> None:
        """
        Write the schema of the DataFrame to the specified location.

        Parameters:
        - df (DataFrame): The DataFrame whose schema is to be written.
        - output_df_params (OutputDataFrameParams): The parameters for writing the DataFrame.

        Raises:
        - ValueError: If there is an issue with writing the schema object to AWS S3.
        """
        pyspark_schema_json = df.schema.jsonValue()

        if output_df_params.dataframe_bucket_params.bucket_name is None:
            raise ValueError("bucket_name must be provided to write schema to S3")

        if output_df_params.dataframe_specific_path:
            if isinstance(output_df_params.dataframe_specific_path, list):
                raise ValueError(
                    "Specific path is set as a list. Only a single path is allowed for writing the schema."
                )
            logger.warning(
                "Specific path is set for writing the schema. Schema will be written to the same path."
            )
            path_to_schema = output_df_params.dataframe_specific_path
        else:
            if output_df_params.dataframe_base_path is None:
                raise ValueError(
                    "Neither 'specific_path' nor 'dataframe_base_path' is set for writing the schema."
                )

            parent_folder_of_dataframe_base_path = "/".join(
                output_df_params.dataframe_base_path.split("/")[:-1]
            )
            path_to_schema = f"{parent_folder_of_dataframe_base_path}/schema.json"

        try:
            self.aws_interface.put_object_aws(
                env=output_df_params.dataframe_bucket_params.env,
                bucket_name=output_df_params.dataframe_bucket_params.bucket_name,
                object_name=path_to_schema,
                object_data=pyspark_schema_json,
            )
        except Exception as e:
            raise ValueError(
                f"Error writing schema to {output_df_params.dataframe_bucket_params.bucket_name}/{path_to_schema}: {e}"
            ) from e

    def _write_dataframe_specific_path(
        self, df: DataFrame, output_df_params: OutputDataFrameParams
    ) -> None:
        bucket_url = self._get_bucket_url(output_df_params.dataframe_bucket_params)
        write_path_url = f"{bucket_url}/{output_df_params.dataframe_specific_path}"

        if output_df_params.overwrite:
            logger.info(
                f"Overwrite is set to True. Deleting existing objects under path {write_path_url}"
            )
            try:
                self.aws_interface.delete_objects_aws(
                    env=output_df_params.dataframe_bucket_params.env,
                    bucket_name=output_df_params.dataframe_bucket_params.bucket_name,
                    path=output_df_params.dataframe_specific_path,
                )
            except Exception as e:
                raise ValueError(f"Error deleting dataframe objects: {e}")

            logger.info("Objects deleted successfully.")

        logger.info(f"Writing DataFrame to path: {write_path_url}...")
        self.spark_manager.write(
            env=output_df_params.dataframe_bucket_params.env,
            df=df,
            path=write_path_url,
            file_type=output_df_params.dataframe_file_type,
            partitions=None,
            coalesce_amount=output_df_params.coalesce_amount,
            repartition_amout=output_df_params.repartition_amout,
        )

    def _write_dataframe_base_path(
        self,
        df: DataFrame,
        output_df_params: OutputDataFrameParams,
    ) -> None:
        """
        Writes a DataFrame to a specified location with optional date partitions.

        Args:
            df (DataFrame): The DataFrame to be written.
            df_params (OutputDataFrameParams): The parameters for writing the DataFrame.

        Returns:
            None
        """
        bucket_url = self._get_bucket_url(output_df_params.dataframe_bucket_params)
        write_base_path_url = f"{bucket_url}/{output_df_params.dataframe_base_path}"
        logger.debug(f"Write base path: {write_base_path_url}")

        write_info = f"Writing DataFrame to base path {write_base_path_url}"
        if output_df_params.partition_by:
            write_info += f" with partitions {output_df_params.partition_by}"
        else:
            write_info += " without partitions"

        df_to_write = df
        date_partition_path = ""
        if output_df_params.single_write_date_params:
            for (
                date_partition,
                date_partition_name,
            ) in output_df_params.single_write_date_params.single_write_date_partitions.items():
                formatted_date_part_value = DATE_FORMATTER[date_partition.value](
                    output_df_params.single_write_date_params.single_write_date
                )
                # Add the date partition column to the DataFrame
                df_to_write = df_to_write.withColumn(
                    date_partition_name, lit(formatted_date_part_value)
                )
                date_partition_path += (
                    f"{date_partition_name}={formatted_date_part_value}/"
                )

            write_info += f". Single write date is being used, so all data will be written to a single path: {write_base_path_url}/{date_partition_path}"

        if output_df_params.overwrite:
            if (
                not date_partition_path
                and output_df_params.dataframe_bucket_params.s3_layer
                not in (S3Layer.GOLD, S3Layer.DIAMOND)
            ):
                logger.warning(
                    "Overwrite is set to True, but single_write_date was not used and this would delete all data in the base path. This is only allowed in the GOLD and DIAMOND layers. Skipping overwrite."
                )
            else:
                full_path = f"{write_base_path_url}/{date_partition_path}"
                logger.info(
                    f"Overwrite is set to True. Deleting existing objects under path {full_path}"
                )
                try:
                    self.aws_interface.delete_objects_aws(
                        env=output_df_params.dataframe_bucket_params.env,
                        bucket_name=output_df_params.dataframe_bucket_params.bucket_name,
                        path=f"{output_df_params.dataframe_base_path}/{date_partition_path}",
                    )
                except Exception as e:
                    raise ValueError(f"Error deleting dataframe objects: {e}")

                logger.info("Objects deleted successfully.")

        logger.info(f"{write_info}...")

        self.spark_manager.write(
            env=output_df_params.dataframe_bucket_params.env,
            df=df_to_write,
            path=write_base_path_url,
            file_type=output_df_params.dataframe_file_type,
            partitions=output_df_params.partition_by,
            coalesce_amount=output_df_params.coalesce_amount,
            repartition_amout=output_df_params.repartition_amout,
        )

        if (
            output_df_params.write_schema_on_s3
            or output_df_params.dataframe_file_type != FileType.PARQUET
        ):
            self.write_schema(df, output_df_params)

    def write_dataframe(
        self,
        df: DataFrame,
        output_df_params: OutputDataFrameParams,
        verbosity: Annotated[int, 0, 2] = 2,
        truncate: Union[int, bool] = False,
        print_schema: bool = False,
    ) -> None:
        """
        Writes a DataFrame to a specified location with optional date partitions.

        Args:
            df (DataFrame): The DataFrame to be written.
            df_params (OutputDataFrameParams): The parameters for writing the DataFrame.

        Returns:
            None
        """
        if df.isEmpty():
            logger.warning("DataFrame is empty. Skipping write operation.")
            return

        if verbosity >= 2:
            logger.info("Starting write operation...")

        if output_df_params.dataframe_base_path:
            self._write_dataframe_base_path(df, output_df_params)
        else:
            self._write_dataframe_specific_path(df, output_df_params)

        if verbosity >= 1:
            logger.info("Dataframe written successfully.")

        if (
            output_df_params.write_schema_on_s3
            or output_df_params.dataframe_file_type != FileType.PARQUET
            or output_df_params.dataframe_bucket_params.s3_layer
            in (S3Layer.GOLD, S3Layer.DIAMOND)
        ):
            if verbosity >= 1:
                logger.info(
                    "write_schema_on_s3 is set to True, or file type is not PARQUET, or S3 layer is GOLD or DIAMOND. Writing schema to S3..."
                )
            self.write_schema(df, output_df_params)
            if verbosity >= 1:
                logger.info("Schema written successfully.")

        if verbosity >= 2:
            logger.info("Write operation completed successfully.\n")

        if verbosity >= 1:
            logger.info("Displaying DataFrame's first row...")
            df.show(1, truncate=truncate)

        if print_schema:
            # Remove partition columns before printing schema
            for col_name in output_df_params.partition_by or []:
                df = df.drop(col_name)

            print("Schema (partition columns removed):")
            df.printSchema()

    @staticmethod
    def read_and_validate_step_json(dataframe_step_params_json_file_path):
        """
        Reads and validates a JSON file containing step parameters.

        Args:
            dataframe_step_params_json_file_path (str): The file path to the JSON file.

        Returns:
            StepParams: An instance of the StepParams class representing the step configuration.

        Raises:
            ValueError: If there is an error loading or decoding the JSON file.
        """
        try:
            with open(dataframe_step_params_json_file_path, "r") as f:
                step_config = json.load(f)
        except (IOError, json.JSONDecodeError) as e:
            raise ValueError(f"Error loading config file: {e}") from e

        return DataFrameStepParams(**step_config)

    def read_input_dataframes_params(
        self,
        input_df_params_dict: InputDataFrameParamsDict,
        verbosity: Annotated[int, 0, 2] = 1,
        truncate: Union[int, bool] = False,
        print_schema: bool = False,
    ) -> DataFrameDict:
        """Reads multiple input dataframes based on the provided configuration."""

        def retry_read_dataframe_previous_dates(
            input_df_params: InputDataFrameParams, max_retries: int = 6
        ):
            for retry in range(max_retries + 1):
                try:
                    df = self.read_dataframe(
                        input_df_params=input_df_params,
                        verbosity=verbosity,
                        truncate=truncate,
                        print_schema=print_schema,
                    )
                    return df
                except EmptyDataFrameException:
                    if retry == max_retries:
                        break

                    assert input_df_params.read_date_params is not None
                    assert isinstance(
                        input_df_params.read_date_params.read_dates, datetime
                    )

                    logger.warning(
                        f"No data found for date {input_df_params.read_date_params.read_dates.strftime('%Y-%m-%d')}. Retrying with previous date..."
                    )
                    input_df_params.read_date_params.read_dates -= timedelta(days=1)
                except (PlaceholderDetectedException, BucketEnvInheritException) as e:
                    logger.error(f"Error reading DataFrame '{df_name}': {e}")
                    raise e

            logger.warning(
                f"End of retry_look_window reached. No data found for the last {max_retries + 1} dates."
            )
            return None

        dfs: DataFrameDict = {}

        for df_name, input_df_params in input_df_params_dict.items():
            if verbosity >= 0:
                logger.info(f"Starting read operation for DataFrame '{df_name}'...")

            if (
                input_df_params.read_date_params
                and input_df_params.read_date_params.was_offset_applied
                and input_df_params.read_date_params.retry_look_window_days > 0
            ):
                df = retry_read_dataframe_previous_dates(
                    input_df_params,
                    max_retries=input_df_params.read_date_params.retry_look_window_days,
                )
            else:
                try:
                    df = self.read_dataframe(
                        input_df_params=input_df_params,
                        verbosity=verbosity,
                        truncate=truncate,
                        print_schema=print_schema,
                    )
                except EmptyDataFrameException:
                    df = None
                except (PlaceholderDetectedException, BucketEnvInheritException) as e:
                    logger.error(f"Error reading DataFrame '{df_name}': {e}")
                    raise e

            if df is not None:
                dfs[df_name] = df
                if verbosity >= 0:
                    logger.info(
                        f"Dataframe '{df_name}' read and added to the dictionary successfully.\n"
                    )
            else:
                if input_df_params.allow_empty_dataframe:
                    logger.warning(
                        f"DATAFRAME '{df_name}' IS EMPTY!! However, since 'allow_empty_dataframe' is set to True, an empty DataFrame will be added to the dictionary for '{df_name}'. Use this with caution!\n"
                    )
                    dfs[df_name] = self.spark_manager.spark_session.createDataFrame(
                        [], schema=StructType([])
                    )
                else:
                    raise EmptyDataFrameException(
                        f"Dataframe '{df_name}' is empty. If you wish to allow empty DataFrames, set 'allow_empty_dataframe' to True in the input_dataframes_params."
                    )
        return dfs

    def apply_transform_function(
        self,
        input_dfs_dict: DataFrameDict,
        transform_params: DataFrameTransformParams,
    ) -> DataFrameDict:
        def extract_partitions(
            df: DataFrame, partition_indexes: list[int] = [0]
        ) -> DataFrame:
            def fetch_partitions(index: int, iterator):
                if index in partition_indexes:
                    return iterator
                else:
                    return []

            rdd = df.rdd
            partitions_rdd = rdd.mapPartitionsWithIndex(fetch_partitions)
            return partitions_rdd.toDF(df.schema)

        transform_fn = transform_params.transform_function

        fn_kwargs = transform_params.fn_kwargs or {}

        logger.info(f"Applying transformation function '{transform_fn.__name__}'...")
        logger.info(f"Function description: {transform_params.transform_description}\n")

        if transform_params.force_extract_partitions is not None:
            logger.warning("Forcing extraction of partitions for all DataFrames...")
            input_dfs_dict = {
                df_name: extract_partitions(
                    df, transform_params.force_extract_partitions
                )
                for df_name, df in input_dfs_dict.items()
            }

        return transform_fn(input_dfs_dict, **fn_kwargs)

    def write_output_dataframes(
        self,
        dfs_to_output: DataFrameDict,
        output_df_params_dict: OutputDataFrameParamsDict,
        verbosity: Annotated[int, 0, 2] = 1,
        truncate: Union[int, bool] = False,
        print_schema: bool = False,
    ) -> None:
        for df_name, df in dfs_to_output.items():
            if verbosity >= 1:
                logger.info(f"Starting write operation for DataFrame '{df_name}'...")
            output_df_params = output_df_params_dict.get(df_name)

            if output_df_params is None:
                raise ValueError(
                    f"No OutputDataFrameParams found for dataframe '{df_name}'"
                )

            self.write_dataframe(
                df, output_df_params, verbosity, truncate, print_schema
            )

    def inject_processing_date_into_dataframe_step_params(
        self, dataframe_step_params: DataFrameStepParams, processing_date: datetime
    ) -> DataFrameStepParams:
        new_dataframe_step_params = dataframe_step_params.model_copy(deep=True)

        for _, df_params in new_dataframe_step_params.input_dataframes_params.items():
            if df_params.read_date_params:
                df_params.read_date_params.was_offset_applied = False

                if df_params.read_date_params.read_dates == "{{processing_date}}":
                    offset = df_params.read_date_params.processing_date_offset_days

                    if offset and offset != 0:
                        df_params.read_date_params.read_dates = (
                            processing_date + timedelta(days=offset)
                        )
                        df_params.read_date_params.was_offset_applied = True
                    else:
                        df_params.read_date_params.read_dates = processing_date

        if new_dataframe_step_params.output_dataframes_params:
            for (
                _,
                df_params,
            ) in new_dataframe_step_params.output_dataframes_params.items():
                if (
                    df_params.single_write_date_params
                    and df_params.single_write_date_params.single_write_date
                    == "{{processing_date}}"
                ):
                    df_params.single_write_date_params.single_write_date = (
                        processing_date
                    )

        return new_dataframe_step_params

    def process_step(
        self,
        dataframe_step_params_json_file_path: Optional[str] = None,
        dataframe_step_params: Optional[DataFrameStepParams] = None,
        processing_date: Optional[datetime] = None,
        write_output_dfs: bool = True,
        return_output_dfs: bool = False,
        verbosity: Annotated[int, 0, 2] = 1,
        truncate: Union[int, bool] = False,
        print_schema: bool = False,
    ) -> Optional[DataFrameDict]:
        """
        Process a step in the data pipeline.

        Args:
            dataframe_step_params_json_file_path (str, optional): The file path to the JSON file containing the step parameters. Either this or `dataframe_step_params` must be provided. Defaults to None.
            dataframe_step_params (StepParams, optional): The step parameters object. Either this or `dataframe_step_params_json_file_path` must be provided. Defaults to None.
            processing_date (datetime, optional): The processing date to be injected into the step parameters. Defaults to None.
            write_output_dfs (bool, optional): Flag indicating whether to write the output DataFrames. Defaults to True.
            return_output_dfs (bool, optional): Flag indicating whether to return the output DataFrames. This is ignored if `write_output_dfs` is False, in which case it is set to True. Defaults to False.

        Returns:
            Optional[DataFrameDict]: A dictionary containing the output DataFrames, if `return_output_dfs` is True.

        Raises:
            ValueError: If neither `dataframe_step_params_json_file_path` nor `dataframe_step_params` is provided, or if both are provided.
            Exception: If an error occurs during the processing step.

        """
        if (
            dataframe_step_params_json_file_path is None
            and dataframe_step_params is None
        ):
            raise ValueError(
                "Either 'dataframe_step_params_json_file_path' or 'dataframe_step_params' must be provided"
            )

        if (
            dataframe_step_params_json_file_path is not None
            and dataframe_step_params is not None
        ):
            raise ValueError(
                "Only one of 'dataframe_step_params_json_file_path' or 'dataframe_step_params' should be provided"
            )

        if dataframe_step_params_json_file_path:
            logger.info("Reading and validating step configuration...")
            dataframe_step_params = self.read_and_validate_step_json(
                dataframe_step_params_json_file_path
            )
            logger.info("Step configuration read and validated.")

        assert (
            dataframe_step_params is not None
        ), "'dataframe_step_params' was unexpectedly None"

        if processing_date is not None:
            logger.debug(
                f"Injecting processing date '{processing_date}' into step parameters..."
            )
            dataframe_step_params = (
                self.inject_processing_date_into_dataframe_step_params(
                    dataframe_step_params=dataframe_step_params,
                    processing_date=processing_date,
                )
            )
            logger.debug("Processing date injected successfully.")

        try:
            print("\nPhase 1: Read Input DataFrames\n" + "-" * 80)
            input_dfs_dict = self.read_input_dataframes_params(
                input_df_params_dict=dataframe_step_params.input_dataframes_params,
                verbosity=verbosity,
                truncate=truncate,
                print_schema=print_schema,
            )
            logger.info("Finished reading Input DataFrames.")

            print("\nPhase 2: Apply Transformation Function\n" + "-" * 80)
            if dataframe_step_params.transform_params:
                dfs_to_output_dict = self.apply_transform_function(
                    input_dfs_dict=input_dfs_dict,
                    transform_params=dataframe_step_params.transform_params,
                )
                logger.info("Transformation function applied successfully.")
            else:
                print("No transformations to apply. Moving to Phase 3.")
                dfs_to_output_dict = input_dfs_dict

            if dataframe_step_params.output_dataframes_params and write_output_dfs:
                print("\nPhase 3: Write Output DataFrames\n" + "-" * 80)
                self.write_output_dataframes(
                    dfs_to_output=dfs_to_output_dict,
                    output_df_params_dict=dataframe_step_params.output_dataframes_params,
                    verbosity=verbosity,
                    truncate=truncate,
                    print_schema=print_schema,
                )
                logger.info("Finished writing Output DataFrames.")

                if return_output_dfs:
                    return dfs_to_output_dict
            else:
                return dfs_to_output_dict
        except Exception as e:
            logger.exception(f"Error during processing step: {e}")
            raise e from None  # Re-raise to propagate the exception

    def process_step_dict(
        self,
        dataframe_step_params_dict: Union[DataFrameStepParamsDict, Dict[str, str]],
        processing_date: Optional[datetime] = None,
        verbosity: Annotated[int, 0, 2] = 1,
        truncate: Union[int, bool] = False,
        print_schema: bool = False,
    ) -> Optional[DataFrameDict]:
        """
        Process a dictionary of step parameters.

        Args:
            dataframe_step_params_dict (Union[StepParamsDict, Dict[str, str]]): A dictionary containing the step IDs as keys and the corresponding step parameters as values.
            processing_date (Optional[datetime], optional): The processing date to be used. Defaults to None.

        Returns:
            Optional[DataFrameDict]: A dictionary containing the processed data frames, if any.

        Raises:
            Exception: If an error occurs during the processing of any step.

        """
        for step_num, (step_id, dataframe_step_params) in enumerate(
            dataframe_step_params_dict.items(), start=1
        ):
            if step_id in self.completed_steps:
                logger.info(f"Step '{step_id}' has already been processed. Skipping...")
                continue
            try:
                if isinstance(dataframe_step_params, str):
                    logger.debug(
                        f"Step params for '{step_id}' is a file path. Reading and validating..."
                    )
                    dataframe_step_params_json_file_path = dataframe_step_params
                    dataframe_step_params = self.read_and_validate_step_json(
                        dataframe_step_params_json_file_path
                    )
                    logger.debug(
                        f"Step params for '{step_id}' read and validated successfully."
                    )

                print("=" * 80)
                print(
                    f"Processing step {step_num}/{len(dataframe_step_params_dict)}: '{step_id}'"
                )
                print("=" * 80)
                self.process_step(
                    dataframe_step_params=dataframe_step_params.model_copy(deep=True),
                    processing_date=processing_date,
                    verbosity=verbosity,
                    truncate=truncate,
                    print_schema=print_schema,
                )

                print("\n" + "-" * 80)
                print(f"Step '{step_id}' processed successfully!\n")
                print("\n" + "-" * 80)

                self.completed_steps.append(step_id)
            except Exception as e:
                logger.exception(f"Error during processing step '{step_id}': {e}")
                raise e from None

        self.completed_steps = []
        print("=" * 80)
        print("All steps processed successfully!")
        print("=" * 80)
