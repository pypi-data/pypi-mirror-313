import json
import os
from orbitkit.util import get_from_dict_or_env
import boto3
from botocore.exceptions import ClientError
import logging

logger = logging.getLogger(__name__)


class SecretManager:
    @staticmethod
    def load_secret_2_env(secret_name: str, override=False, region_name="us-west-2", *args, **kwargs):
        # Create a Secrets Manager client
        session = boto3.session.Session()

        try:
            # Try to get aws keys
            aws_access_key_id = get_from_dict_or_env(
                kwargs, "aws_access_key_id", "AWS_ACCESS_KEY_ID",
            )
            aws_secret_access_key = get_from_dict_or_env(
                kwargs, "aws_secret_access_key", "AWS_SECRET_ACCESS_KEY",
            )
            client = session.client(
                service_name='secretsmanager',
                region_name=region_name,
                aws_access_key_id=aws_access_key_id,
                aws_secret_access_key=aws_secret_access_key,
            )
        except:
            client = session.client(
                service_name='secretsmanager',
                region_name=region_name,
            )

        try:
            get_secret_value_response = client.get_secret_value(
                SecretId=secret_name
            )
        except ClientError as e:
            # For a list of exceptions thrown, see
            # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
            raise e

        logger.warning(f"Please be noticed that loading [{secret_name}] from AWS Secret Manager successfully.")
        secret = get_secret_value_response['SecretString']

        # Set all key/value to env
        all_secrets = json.loads(secret)
        for key, value in all_secrets.items():
            if override:
                os.environ[key] = value
            else:
                os.environ.setdefault(key, value)

    @staticmethod
    def load_secret_2_envs(secret_names: list, override=False, region_name="us-west-2", *args, **kwargs):
        if len(secret_names) <= 0:
            raise Exception("Must provide at least one secret name.")

        for secret_name in secret_names:
            SecretManager.load_secret_2_env(secret_name, override=override, region_name=region_name, *args, **kwargs)


if __name__ == "__main__":
    # SecretManager.load_secret_2_env("demo")
    SecretManager.load_secret_2_envs(["demo1", "demo2"])
    print(os.environ["abc"])
