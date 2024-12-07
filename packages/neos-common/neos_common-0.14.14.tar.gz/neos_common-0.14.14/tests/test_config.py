from unittest import mock

import neos_common.config
from neos_common.config import Config


class TestConfig:
    def test_load(self, monkeypatch):
        monkeypatch.setenv("NC_POSTGRES_HOST", "host")
        monkeypatch.setenv("NC_POSTGRES_USER", "user")
        monkeypatch.setenv("NC_POSTGRES_DATABASE", "database")
        monkeypatch.setenv("NC_POSTGRES_PASSWORD", "pword")
        monkeypatch.setattr(neos_common.config.dotenv, "find_dotenv", mock.Mock(return_value=""))

        Config.load()

        assert neos_common.config.dotenv.find_dotenv.call_args == mock.call(usecwd=True)

    def test_postgres_dsn(self, monkeypatch):
        monkeypatch.setenv("NC_POSTGRES_HOST", "host")
        monkeypatch.setenv("NC_POSTGRES_USER", "user")
        monkeypatch.setenv("NC_POSTGRES_DATABASE", "database")
        monkeypatch.setenv("NC_POSTGRES_PASSWORD", "pword")

        config = Config()

        dsn = config.postgres_dsn

        assert dsn == "postgresql://user:pword@host:5432/database"

    def test_logging_config(self, monkeypatch):
        monkeypatch.setenv("NC_POSTGRES_HOST", "host")
        monkeypatch.setenv("NC_POSTGRES_USER", "user")
        monkeypatch.setenv("NC_POSTGRES_DATABASE", "database")
        monkeypatch.setenv("NC_POSTGRES_PASSWORD", "pword")

        config = Config()

        assert config.logging_config == {
            "disable_existing_loggers": True,
            "formatters": {
                "default": {
                    "datefmt": "%Y-%m-%d %H:%M:%S",
                    "format": "[%(asctime)s][%(name)s][%(levelname)s]: %(message)s",
                },
            },
            "handlers": {
                "default": {
                    "class": "logging.StreamHandler",
                    "formatter": "default",
                    "level": "INFO",
                },
            },
            "loggers": {
                "common": {
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
                    "level": "INFO",
                    "propagate": False,
                },
            },
            "version": 1,
        }
