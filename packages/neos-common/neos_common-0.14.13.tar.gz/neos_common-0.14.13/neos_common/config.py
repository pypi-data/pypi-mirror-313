import typing as t

import dotenv
import pydantic
import pydantic_settings

T = t.TypeVar("T", bound=pydantic.BaseModel)


class Config(pydantic_settings.BaseSettings):
    """Service configuration base class."""

    @classmethod
    def load(cls: type[T]) -> T:
        env = dotenv.find_dotenv(usecwd=True)

        return cls(_env_file=env)

    model_config = pydantic_settings.SettingsConfigDict(
        env_prefix="nc_",
        extra="ignore",
    )

    name: str = "common"

    logging_level: str = pydantic.Field(default="INFO")

    # -- DATABASE --

    postgres_host: str
    postgres_user: str
    postgres_database: str
    postgres_password: str
    postgres_port: int = pydantic.Field(default=5432)

    postgres_pool_min_size: int = pydantic.Field(default=1)
    postgres_pool_max_size: int = pydantic.Field(default=1)

    @property
    def postgres_dsn(self) -> str:
        """Generate postgres dsn from provided configuration."""
        auth = f"{self.postgres_user}:{self.postgres_password}"
        host = f"{self.postgres_host}:{self.postgres_port}"
        return f"postgresql://{auth}@{host}/{self.postgres_database}"

    @property
    def logging_config(self) -> dict:
        """Generate default logging config."""
        return {
            "version": 1,
            "disable_existing_loggers": True,
            "formatters": {
                "default": {
                    "format": "[%(asctime)s][%(name)s][%(levelname)s]: %(message)s",
                    "datefmt": "%Y-%m-%d %H:%M:%S",
                },
            },
            "handlers": {
                "default": {
                    "class": "logging.StreamHandler",
                    "level": self.logging_level.upper(),
                    "formatter": "default",
                },
            },
            "loggers": {
                self.name: {
                    "handlers": ["default"],
                    "level": self.logging_level.upper(),
                    "propagate": False,
                },
                "pogo_migrate": {
                    "handlers": ["default"],
                    "level": "INFO",
                    "propagate": False,
                },
                "neos_common": {
                    "handlers": ["default"],
                    "level": self.logging_level.upper(),
                    "propagate": False,
                },
            },
        }


class ApiConfig(Config):
    """API Service configuration base class."""

    name: str = "common-api"

    raw_api_prefix: str = pydantic.Field(default="", alias="NC_API_PREFIX")

    @property
    def api_prefix(self) -> str:
        """Ensure api prefix starts with /."""
        api_prefix = self.raw_api_prefix
        if api_prefix and not api_prefix.startswith("/"):
            api_prefix = f"/{api_prefix}"
        return api_prefix

    # -- KEYCLOAK --

    keycloak_host: str
    keycloak_realm: str
    keycloak_client_id: str
    keycloak_client_secret: str

    # -- ACCESS SECRET --
    access_key_id: str
    secret_access_key: str
    partition: str = pydantic.Field(default="ksa")

    @property
    def logging_config(self) -> dict:
        """Generate default logging config including api loggers."""
        return {
            "version": 1,
            "disable_existing_loggers": True,
            "formatters": {
                "default": {
                    "format": "[%(asctime)s][%(name)s][%(levelname)s]: %(message)s",
                    "datefmt": "%Y-%m-%d %H:%M:%S",
                },
            },
            "handlers": {
                "default": {
                    "class": "logging.StreamHandler",
                    "level": self.logging_level.upper(),
                    "formatter": "default",
                },
            },
            "loggers": {
                self.name: {
                    "handlers": ["default"],
                    "level": self.logging_level.upper(),
                    "propagate": False,
                },
                "uvicorn.access": {
                    "handlers": ["default"],
                    "level": "INFO",
                    "propagate": False,
                },
                "pogo_migrate": {
                    "handlers": ["default"],
                    "level": "INFO",
                    "propagate": False,
                },
                "neos_common": {
                    "handlers": ["default"],
                    "level": self.logging_level.upper(),
                    "propagate": False,
                },
            },
        }
