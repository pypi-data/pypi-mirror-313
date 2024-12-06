Module neos_common.config
=========================

Classes
-------

`ApiConfig(**values: Any)`
:   API Service configuration base class.
    
    Create a new model by parsing and validating input data from keyword arguments.
    
    Raises [`ValidationError`][pydantic_core.ValidationError] if the input data cannot be
    validated to form a valid model.
    
    `self` is explicitly positional-only to allow `self` as a field name.

    ### Ancestors (in MRO)

    * neos_common.config.Config
    * pydantic_settings.main.BaseSettings
    * pydantic.main.BaseModel

    ### Class variables

    `access_key_id: str`
    :

    `keycloak_client_id: str`
    :

    `keycloak_client_secret: str`
    :

    `keycloak_host: str`
    :

    `keycloak_realm: str`
    :

    `model_computed_fields`
    :

    `model_config: ClassVar[pydantic_settings.main.SettingsConfigDict]`
    :

    `model_fields`
    :

    `name: str`
    :

    `partition: str`
    :

    `raw_api_prefix: str`
    :

    `secret_access_key: str`
    :

    ### Instance variables

    `api_prefix: str`
    :   Ensure api prefix starts with /.

    `logging_config: dict`
    :   Generate default logging config including api loggers.

`Config(**values: Any)`
:   Service configuration base class.
    
    Create a new model by parsing and validating input data from keyword arguments.
    
    Raises [`ValidationError`][pydantic_core.ValidationError] if the input data cannot be
    validated to form a valid model.
    
    `self` is explicitly positional-only to allow `self` as a field name.

    ### Ancestors (in MRO)

    * pydantic_settings.main.BaseSettings
    * pydantic.main.BaseModel

    ### Descendants

    * neos_common.config.ApiConfig

    ### Class variables

    `logging_level: str`
    :

    `model_computed_fields`
    :

    `model_config: ClassVar[pydantic_settings.main.SettingsConfigDict]`
    :

    `model_fields`
    :

    `name: str`
    :

    `postgres_database: str`
    :

    `postgres_host: str`
    :

    `postgres_password: str`
    :

    `postgres_pool_max_size: int`
    :

    `postgres_pool_min_size: int`
    :

    `postgres_port: int`
    :

    `postgres_user: str`
    :

    ### Static methods

    `load() ‑> ~T`
    :

    ### Instance variables

    `logging_config: dict`
    :   Generate default logging config.

    `postgres_dsn: str`
    :   Generate postgres dsn from provided configuration.