import json
import os
from typing import Dict, List

import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv

from tommytomato_utils.load_secrets.environment import Environment
from tommytomato_utils.load_secrets.exceptions import (
    ErrorWhenReadingInSecretsFromAWSSecretsManagerError
)


class SecretsLoader:

    def __init__(self, environment: Environment):
        self.environment = environment
        self.load_env_files()

    def load_env_files(self):
        # Load the base .env file
        base_dir = os.path.abspath(os.path.dirname(__name__))
        env_path = os.path.join(base_dir, 'credentials/.env')

        load_dotenv(env_path)

    def validate_secrets(self, secrets: Dict[str, str], required_secrets: List[str]) -> None:
        missing_secrets = [
            key for key in required_secrets if key not in secrets or secrets[key] is None
        ]
        if missing_secrets:
            raise ValueError(f"The following secrets are missing: {', '.join(missing_secrets)}")

    def load_from_env(self, required_secrets: List[str]) -> Dict[str, str]:
        secrets = {key: os.getenv(key)
                   for key in required_secrets}
        return secrets

    def load_from_aws(self, required_secrets: List[str]) -> Dict[str, str]:
        secret_name = f"{self.environment.name.lower()}/ops-tooling"
        region_name = "eu-central-1"

        # Create a Secrets Manager client
        session = boto3.session.Session()
        client = session.client(service_name='secretsmanager', region_name=region_name)

        try:
            get_secret_value_response = client.get_secret_value(SecretId=secret_name)
        except ClientError as exception:
            raise ErrorWhenReadingInSecretsFromAWSSecretsManagerError(
                secret_name,
                region_name,
                exception,
            )

        secret = get_secret_value_response['SecretString']
        aws_secrets = json.loads(secret)

        # Only return the required secrets
        secrets = {key: aws_secrets.get(key)
                   for key in required_secrets}
        return secrets

    def load_secrets(self, required_secrets: List[str]) -> Dict[str, str]:
        # Load secrets from .env
        secrets = self.load_from_env(required_secrets)

        # Check for missing secrets
        missing_secrets = [key for key, value in secrets.items() if value is None]

        if missing_secrets:
            # Load missing secrets from AWS
            aws_secrets = self.load_from_aws(missing_secrets)
            secrets.update(aws_secrets)

        # Validate all required secrets are now present
        self.validate_secrets(secrets, required_secrets)
        return secrets
