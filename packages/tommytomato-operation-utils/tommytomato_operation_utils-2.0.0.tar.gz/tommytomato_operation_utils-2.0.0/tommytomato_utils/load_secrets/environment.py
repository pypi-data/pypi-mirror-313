from enum import Enum
from typing import List


class Environment(Enum):
    """Contains all valid Environments"""
    TESTING = "TESTING"
    ACCEPTANCE = "ACCEPTANCE"
    PRODUCTION = "PRODUCTION"

    def __str__(self) -> str:
        return str(self.value)

    @classmethod
    def possible_environment_values(cls) -> List[str]:
        return [environment.value for environment in Environment]

    @classmethod
    def from_str(cls, env_str: str) -> 'Environment':
        if env_str is None:
            raise ValueError(
                "Environment string is None. "
                f"Valid environments are: {cls.possible_environment_values()}"
            )

        for env in cls:
            if env.value.lower() == env_str.lower():
                return env

        raise ValueError(
            f"Invalid environment: {env_str}. "
            f"Valid environments are: {cls.possible_environment_values()}"
        )
