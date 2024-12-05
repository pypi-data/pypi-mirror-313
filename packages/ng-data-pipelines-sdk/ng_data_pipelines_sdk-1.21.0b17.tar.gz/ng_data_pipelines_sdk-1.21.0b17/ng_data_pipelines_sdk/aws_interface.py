import json
from typing import Dict, Optional

import boto3

from ng_data_pipelines_sdk.interfaces import AWSCredentials, Env


class AWSServiceClient:
    """
    A class representing an AWS service client.

    This class provides a convenient way to interact with various AWS services,
    such as S3 and Secrets Manager, by encapsulating the necessary client and
    resource objects.

    Args:
        region_name (str, optional): The AWS region name. Defaults to None.
        aws_credentials (AWSCredentials, optional): The AWS credentials. Defaults to None.
    """

    def __init__(
        self,
        region_name: Optional[str] = None,
        aws_credentials: Optional[AWSCredentials] = None,
    ):
        region_name = region_name if region_name else None
        aws_access_key_id = (
            aws_credentials.aws_access_key_id if aws_credentials else None
        )
        aws_secret_access_key = (
            aws_credentials.aws_secret_access_key if aws_credentials else None
        )

        self.s3_client = boto3.client(
            "s3",
            region_name=region_name,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
        )
        self.s3_resource = boto3.resource(
            "s3",
            region_name=region_name,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
        )
        self.secrets_manager_client = boto3.client(
            "secretsmanager",
            region_name=region_name,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
        )


class AWSInterface:
    """
    A class that provides an interface for interacting with AWS services.

    Args:
        region_name (str): The name of the AWS region.
        aws_credentials_dict (Optional[Dict[Env, AWSCredentials]]): A dictionary containing AWS credentials for different environments. Defaults to None.

    Attributes:
        client_managers (Dict[Env, AWSServiceClient]): A dictionary that maps environment to AWSServiceClient instances.

    """

    def __init__(
        self,
        region_name: str,
        aws_credentials_dict: Optional[Dict[Env, AWSCredentials]] = None,
    ):
        if not aws_credentials_dict:
            self.client_managers = {
                env: AWSServiceClient(region_name=region_name)
                for env in [Env.DEV, Env.PRD, Env.STG]
            }
        else:
            self.client_managers = {
                env: AWSServiceClient(
                    region_name=region_name, aws_credentials=credentials
                )
                for env, credentials in aws_credentials_dict.items()
            }

    def get_service_client(self, env: Env) -> AWSServiceClient:
        """
        Get the AWSServiceClient instance for the specified environment.

        Args:
            env (Env): The environment for which to get the AWSServiceClient.

        Returns:s
            AWSServiceClient: The AWSServiceClient instance.

        Raises:
            ValueError: If no AWS credentials are found for the specified environment.

        """
        if env not in self.client_managers:
            raise ValueError(f"No AWS credentials found for environment {env}")

        return self.client_managers[env]

    def get_object_aws(self, env: Env, bucket_name: str, object_name: str) -> bytes:
        """
        Get the contents of an object from an AWS S3 bucket.

        Args:
            env (Env): The environment in which the bucket is located.
            bucket_name (str): The name of the bucket.
            object_name (str): The name of the object.

        Returns:
            bytes: The contents of the object.

        """
        client_manager = self.get_service_client(env)
        response = client_manager.s3_client.get_object(
            Bucket=bucket_name, Key=object_name
        )
        return response["Body"].read()

    def put_object_aws(
        self, env: Env, bucket_name: str, object_name: str, object_data: dict
    ) -> None:
        """
        Put an object into an AWS S3 bucket.

        Args:
            env (Env): The environment in which the bucket is located.
            bucket_name (str): The name of the bucket.
            object_name (str): The name of the object.
            object_data (dict): The data to be stored in the object.

        Returns:
            None

        """
        client_manager = self.get_service_client(env)
        client_manager.s3_client.put_object(
            Bucket=bucket_name,
            Key=object_name,
            Body=bytes(json.dumps(object_data), encoding="UTF-8"),
        )

    def put_file_aws(self, env: Env, bucket_name: str, object_name: str, file) -> None:
        """
        Put a file into an AWS S3 bucket.

        Args:
            env (Env): The environment in which the bucket is located.
            bucket_name (str): The name of the bucket.
            object_name (str): The name of the object.
            file: The file to be stored in the bucket.

        Returns:
            None

        """
        client_manager = self.get_service_client(env)
        client_manager.s3_client.put_object(
            Bucket=bucket_name,
            Key=object_name,
            Body=file,
        )

    @staticmethod
    def concat_multiple_data_events(events):
        """
        Concatenate multiple data events into a single string.

        Args:
            events: The list of data events to be concatenated.

        Returns:
            str: The concatenated data events.

        """
        mult_data = ""

        for event in events:
            mult_data += json.dumps(event) + "\n"

        return mult_data[:-1].encode("UTF-8")

    def put_multiple_objects_aws_single_file(
        self, env: Env, bucket_name, object_name, objects
    ):
        """
        Put multiple objects into an AWS S3 bucket using a single file.

        Args:
            env (Env): The environment in which the bucket is located.
            bucket_name (str): The name of the bucket.
            object_name (str): The name of the object.
            objects: The list of objects to be stored in the bucket.

        Returns:
            None

        """
        client_manager = self.get_service_client(env)

        concat_mult_objects = self.concat_multiple_data_events(objects)

        return client_manager.s3_client.put_object(
            Bucket=bucket_name,
            Key=object_name,
            Body=concat_mult_objects,
        )

    def list_objects_key_aws(self, env: Env, bucket_name, path):
        """
        List the keys of objects in an AWS S3 bucket.

        Args:
            env (Env): The environment in which the bucket is located.
            bucket_name (str): The name of the bucket.
            path (str): The path to filter the objects.

        Returns:
            List[str]: The keys of the objects.

        """
        client_manager = self.get_service_client(env)

        bucket_resource = client_manager.s3_resource.Bucket(bucket_name)  # type: ignore
        objects_key = []

        for object_summary in bucket_resource.objects.filter(Prefix=path):
            objects_key.append(object_summary.key)

        return objects_key

    def list_objects_url_aws(self, env: Env, bucket_name, path):
        """
        List the URLs of objects in an AWS S3 bucket.

        Args:
            env (Env): The environment in which the bucket is located.
            bucket_name (str): The name of the bucket.
            path (str): The path to filter the objects.

        Returns:
            List[str]: The URLs of the objects.

        """
        client_manager = self.get_service_client(env)

        bucket_resource = client_manager.s3_resource.Bucket(bucket_name)  # type: ignore
        objects_url = []

        for object_summary in bucket_resource.objects.filter(Prefix=path):
            objects_url.append(
                f"s3://{object_summary.bucket_name}/{object_summary.key}"
            )

        return objects_url

    def delete_objects_aws(self, env: Env, bucket_name, path):
        """
        Delete objects from an AWS S3 bucket.

        Args:
            env (Env): The environment in which the bucket is located.
            bucket_name (str): The name of the bucket.
            path (str): The path to filter the objects.

        Returns:
            None

        """
        client_manager = self.get_service_client(env)

        bucket = client_manager.s3_resource.Bucket(bucket_name)  # type: ignore
        return bucket.objects.filter(Prefix=path).delete()

    def get_secret_aws(self, env: Env, secret_name: str) -> dict:
        """
        Get the value of a secret from AWS Secrets Manager.

        Args:
            env (Env): The environment in which the secret is located.
            secret_name (str): The name of the secret.

        Returns:
            dict: The value of the secret.

        """
        client_manager = self.get_service_client(env)

        get_secret_value_response = (
            client_manager.secrets_manager_client.get_secret_value(SecretId=secret_name)
        )
        return json.loads(get_secret_value_response["SecretString"])
