import os
from dataclasses import dataclass, asdict, field
from enum import Enum

import yaml


class Environment(str, Enum):
    LOCAL = "local"
    STAGING = "staging"
    PROD = "prod"


@dataclass(slots=True, frozen=True)
class EnvConfig:
    environment: Environment
    keycloak_url: str
    client_id: str
    grant_type: str
    scopes: [str]
    client_secret: str = field(repr=False)
    redirect_host: str = field(repr=False)
    redirect_port: int = field(repr=False)
    raw: dict = field(repr=False, default_factory=dict)

    @staticmethod
    def from_env(env: Environment, file: str = "./config.yaml") -> 'EnvConfig':
        with open(file) as config_file:
            config = yaml.safe_load(config_file)
        env_config = config[env.lower()]
        return EnvConfig(
            environment=Environment[env.upper()],
            keycloak_url=env_config.get("keycloak_url") or os.getenv("KEYCLOAK_URL"),
            grant_type=env_config.get("grant_type") or os.getenv("GRANT_TYPE"),
            redirect_host=env_config.get("redirect_host") or os.getenv("REDIRECT_URL"),
            redirect_port=env_config.get("redirect_port") or os.getenv("REDIRECT_PORT"),
            client_id=env_config.get("client_id") or os.getenv("CLIENT_ID"),
            client_secret=env_config.get("client_secret") or os.getenv("CLIENT_SECRET"),
            scopes=env_config.get("scopes") or os.getenv("SCOPES"),
            raw=env_config)

    def __post_init__(self):
        if self.environment is not Environment.LOCAL:
            empty_fields = [k for k, v in asdict(self).items() if v is None]
            if empty_fields:
                raise Exception(f"{empty_fields} are not set!")
