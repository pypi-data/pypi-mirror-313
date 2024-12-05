import functools
import time
from typing import Any, Callable, Dict, List, Optional, Union

from pyspark.conf import SparkConf
from pyspark.sql import SparkSession
from pyspark.sql.dataframe import DataFrame
from pyspark.sql.types import StructType

from ng_data_pipelines_sdk.custom_logger import logger
from ng_data_pipelines_sdk.interfaces import (
    AWSCredentials,
    Env,
    FileType,
    HadoopS3FileSystem,
    SparkConfigParams,
)


def retry_operation(retries: int, delay: int, backoff: int):
    """
    Decorator for retrying a function if an exception is raised.

    Args:
        tries (int): Number of times to try before giving up.
        delay (int): Initial delay between retries in seconds.
        backoff (int): Multiplier by which the delay should be increased after each failure.

    Returns:
        Callable: The wrapped function.
    """

    def decorator_retry(func: Callable):
        @functools.wraps(func)
        def wrapper_retry(*args, **kwargs) -> Any:
            attempts = 0
            current_delay = delay
            while attempts <= retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    logger.error(f"Attempt {attempts + 1} failed with error:\n")
                    print(f"```\n{e}\n```\n")
                    logger.info(f"Retrying in {current_delay} seconds...")
                    time.sleep(current_delay)
                    attempts += 1
                    current_delay *= backoff

            raise Exception(f"Operation failed after {retries} attempts")

        return wrapper_retry

    return decorator_retry


class SparkManager:
    """
    A class that manages the SparkSession and provides methods for reading and writing data.

    Args:
        app_name (str): The name of the Spark application.
        aws_credentials_dict (Optional[Dict[Env, AWSCredentials]], optional): A dictionary of AWS credentials for each environment. Defaults to None.
        hadoop_s3_file_system (Optional[HadoopS3FileSystem], optional): The Hadoop S3 file system to use. Defaults to None. If AWS credentials are provided, this must be provided as well.
        spark_config_params (SparkConfigParams, optional): The Spark configuration parameters. Defaults to SparkConfigParams().
    """

    def __init__(
        self,
        app_name: str = "Spark Application",
        aws_credentials_dict: Optional[Dict[Env, AWSCredentials]] = None,
        hadoop_s3_file_system: Optional[HadoopS3FileSystem] = None,
        spark_config_params: SparkConfigParams = SparkConfigParams(),
    ):
        self.aws_credentials_dict = aws_credentials_dict

        if aws_credentials_dict and hadoop_s3_file_system is None:
            raise ValueError(
                "If AWS credentials are provided, the Hadoop S3 file system must also be provided."
            )

        self.hadoop_s3_file_system = hadoop_s3_file_system
        spark_config = self.create_spark_config(app_name, spark_config_params)

        spark_session_builder = SparkSession.Builder().config(conf=spark_config)
        self.spark_session = spark_session_builder.getOrCreate()

    def _set_aws_credentials(self, env: Env):
        """
        Sets the AWS credentials for the specified environment.

        Args:
            env (Env): The environment for which to set the AWS credentials.
        """
        if not self.aws_credentials_dict:
            return

        aws_credentials = self.aws_credentials_dict[env]

        jsc = getattr(self.spark_session.sparkContext, "_jsc")
        hadoopConfiguration = jsc.hadoopConfiguration()

        aws_access_key_config_name = (
            "fs.s3.awsAccessKeyId"
            if self.hadoop_s3_file_system == HadoopS3FileSystem.S3
            else "fs.s3a.access.key"
        )

        aws_secret_access_key_config_name = (
            "fs.s3.awsSecretAccessKey"
            if self.hadoop_s3_file_system == HadoopS3FileSystem.S3
            else "fs.s3a.secret.key"
        )

        hadoopConfiguration.set(
            aws_access_key_config_name, aws_credentials.aws_access_key_id
        )

        hadoopConfiguration.set(
            aws_secret_access_key_config_name, aws_credentials.aws_secret_access_key
        )

        logger.debug(f"Set AWS credentials for {env} environment.")

    def create_spark_config(
        self,
        app_name: str,
        spark_config_params: SparkConfigParams,
    ):
        """
        Creates the Spark configuration.

        Args:
            app_name (str): The name of the Spark application.

        Returns:
            SparkConf: The Spark configuration.
        """
        # Convert the Pydantic model to a dictionary

        config: SparkConf = SparkConf().setAppName(app_name)

        # Apply configurations, ignoring any that are None
        config_params = spark_config_params.model_dump(
            mode="json",
            by_alias=True,
            exclude_none=True,
            exclude={"additional_configs"},
        )

        additional_configs = spark_config_params.additional_configs or {}

        all_configs = {**config_params, **additional_configs}

        for key, value in all_configs.items():
            config.set(key, value)

        config.set("spark.sql.parquet.datetimeRebaseModeInRead", "LEGACY")
        config.set("spark.sql.parquet.datetimeRebaseModeInWrite", "LEGACY")
        config.set("spark.sql.parquet.int96RebaseModeInWrite", "LEGACY")
        config.set("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")

        if self.aws_credentials_dict:
            config.set(
                "spark.hadoop.fs.s3a.aws.credentials.provider",
                "org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider",
            )
        else:
            config.set(
                "spark.hadoop.fs.s3a.aws.credentials.provider",
                "com.amazonaws.auth.InstanceProfileCredentialsProvider",
            )

        return config

    @retry_operation(retries=3, delay=2, backoff=2)
    def read(
        self,
        env: Env,
        paths: Union[str, List[str]],
        file_type: FileType,
        base_path: Optional[str] = None,
        schema: Optional[StructType] = None,
        persist: bool = False,
    ) -> Optional[DataFrame]:
        def get_existing_paths(paths: List[str]) -> List[str]:
            spark_context = self.spark_session.sparkContext
            hadoop_conf = spark_context._jsc.hadoopConfiguration()  # type: ignore
            existing_paths = []
            for path in paths:
                fs_path = self.spark_session._jvm.org.apache.hadoop.fs.Path(path)  # type: ignore
                fs = fs_path.getFileSystem(hadoop_conf)  # type: ignore
                if fs.exists(fs_path):
                    existing_paths.append(path)
                else:
                    logger.warning(f"Path does not exist (ignoring): {path}")

            return existing_paths

        self._set_aws_credentials(env)

        if isinstance(paths, str):
            paths = [paths]

        existing_paths = get_existing_paths(paths)

        if existing_paths == []:
            logger.warning("No existing paths found.")
            return None

        logger.info(f"Reading data from existing paths: {existing_paths}")

        reader = self.spark_session.read.format(file_type)
        if schema:
            reader = reader.schema(schema)
        if base_path:
            reader = reader.option("basePath", base_path)

        df = reader.load(existing_paths)

        if persist:
            logger.info("Caching DataFrame...")
            df.persist()
            df.count()  # Trigger persistence

        return df

    @retry_operation(retries=1, delay=2, backoff=2)
    def write(
        self,
        env: Env,
        df: DataFrame,
        path: str,
        file_type: FileType,
        partitions: Optional[List[str]] = None,
        coalesce_amount: Optional[int] = None,
        repartition_amout: Optional[int] = None,
    ):
        """
        Writes the DataFrame to the specified path using the specified file type.

        Args:
            env (Env): The environment to use for setting AWS credentials.
            df (DataFrame): The DataFrame to write.
            path (str): The path where the DataFrame should be written.
            file_type (FileType): The file type to use for writing the DataFrame.
            partitions (Optional[List[str]], optional): A list of partition columns to use for writing the DataFrame. Defaults to None.
            coalesce (Optional[int], optional): The number of partitions to coalesce the DataFrame into before writing. Defaults to None.
            repartition (Optional[int], optional): The number of partitions to repartition the DataFrame into before writing. Defaults to None.
        """
        self._set_aws_credentials(env)

        if coalesce_amount:
            df = df.coalesce(coalesce_amount)

        if repartition_amout:
            df = df.repartition(repartition_amout)

        if partitions:
            df.write.partitionBy(partitions).format(file_type).mode("append").save(path)
        else:
            df.write.format(file_type).mode("append").save(path)
