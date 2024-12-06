class ErrorWhenReadingInSecretsFromAWSSecretsManagerError(Exception):

    def __init__(self, secret_name: str, region_name: str, exception: Exception):
        super().__init__(
            "An error occurred when reading in secrets from AWS Secrets Manager. "
            f"\nThe following error occurred: {exception}\n\n"
            "Secrets are gathered from:\n\n"
            f"-secret_name: {secret_name}\n"
            f"-region_name: {region_name}\n"
        )
