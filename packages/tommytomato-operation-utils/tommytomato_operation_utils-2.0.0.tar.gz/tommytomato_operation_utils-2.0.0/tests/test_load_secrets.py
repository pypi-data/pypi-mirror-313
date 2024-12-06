import unittest
from unittest.mock import patch

from tommytomato_utils.load_secrets.environment import Environment
from tommytomato_utils.load_secrets.secrets_loader import SecretsLoader


class TestSecretsLoader(unittest.TestCase):

    def setUp(self):
        self.environment = Environment.TESTING

    @patch('tommytomato_utils.load_secrets.secrets_loader.load_dotenv')
    def test_load_env_files(self, mock_load_dotenv):
        secrets_loader = SecretsLoader(self.environment)
        secrets_loader.load_env_files()
        mock_load_dotenv.assert_called()

    @patch('os.getenv')
    def test_load_from_env(self, mock_getenv):
        secrets_loader = SecretsLoader(self.environment)
        required_secrets = ['SECRET_KEY']
        mock_getenv.return_value = 'mocked_secret_value'
        secrets = secrets_loader.load_from_env(required_secrets)
        self.assertEqual(secrets['SECRET_KEY'], 'mocked_secret_value')

    @patch('boto3.session.Session.client')
    def test_load_from_aws(self, mock_boto_client):
        secrets_loader = SecretsLoader(self.environment)
        required_secrets = ['AWS_SECRET_KEY']
        mock_client_instance = mock_boto_client.return_value
        mock_client_instance.get_secret_value.return_value = {
            'SecretString': '{"AWS_SECRET_KEY": "aws_mocked_secret_value"}'
        }
        secrets = secrets_loader.load_from_aws(required_secrets)
        self.assertEqual(secrets['AWS_SECRET_KEY'], 'aws_mocked_secret_value')

    def test_validate_secrets(self):
        secrets_loader = SecretsLoader(self.environment)
        secrets = {
            'SECRET_KEY': 'mocked_secret_value'
        }
        required_secrets = ['SECRET_KEY']
        secrets_loader.validate_secrets(secrets, required_secrets)

    def test_validate_secrets_missing(self):
        secrets_loader = SecretsLoader(self.environment)
        secrets = {}
        required_secrets = ['SECRET_KEY']
        with self.assertRaises(ValueError):
            secrets_loader.validate_secrets(secrets, required_secrets)
