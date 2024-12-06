Module neos_common.event
========================

Classes
-------

`ClassificationResult(**data: Any)`
:   Data classification results model.
    
    Create a new model by parsing and validating input data from keyword arguments.
    
    Raises [`ValidationError`][pydantic_core.ValidationError] if the input data cannot be
    validated to form a valid model.
    
    `self` is explicitly positional-only to allow `self` as a field name.

    ### Ancestors (in MRO)

    * pydantic.main.BaseModel

    ### Class variables

    `column_results: dict`
    :

    `config: dict`
    :

    `dataset_type: str`
    :

    `entity_identifier: uuid.UUID`
    :

    `id_: uuid.UUID`
    :

    `model_computed_fields`
    :

    `model_config`
    :

    `model_fields`
    :

`Emitter(session_id: uuid.UUID | None = None)`
:   Helper class that provides a standard way to create an ABC using
    inheritance.

    ### Ancestors (in MRO)

    * abc.ABC

    ### Descendants

    * neos_common.event.TmpEmitter

    ### Methods

    `emit(self, event_packet: neos_common.event.EventPacket) ‑> None`
    :

`Event(emitter: neos_common.event.Emitter, source: str = 'source', session_id: Optional[Annotated[uuid.UUID, UuidVersion(uuid_version=4), PlainSerializer(func=<function <lambda> at 0x76475c731b20>, return_type=PydanticUndefined, when_used='always')]] = None)`
:   Helper class that provides a standard way to create an ABC using
    inheritance.

    ### Ancestors (in MRO)

    * abc.ABC

    ### Methods

    `emit(self, message: str, span_id: Optional[Annotated[uuid.UUID, UuidVersion(uuid_version=4), PlainSerializer(func=<function <lambda> at 0x76475c731b20>, return_type=PydanticUndefined, when_used='always')]] = None, message_type: str = 'unknown', session_id: Optional[Annotated[uuid.UUID, UuidVersion(uuid_version=4), PlainSerializer(func=<function <lambda> at 0x76475c731b20>, return_type=PydanticUndefined, when_used='always')]] = None) ‑> uuid.UUID`
    :

    `version(self) ‑> neos_common.event.EventVersion`
    :

`EventAction(*args, **kwds)`
:   Create a collection of name/value pairs.
    
    Example enumeration:
    
    >>> class Color(Enum):
    ...     RED = 1
    ...     BLUE = 2
    ...     GREEN = 3
    
    Access them by:
    
    - attribute access:
    
      >>> Color.RED
      <Color.RED: 1>
    
    - value lookup:
    
      >>> Color(1)
      <Color.RED: 1>
    
    - name lookup:
    
      >>> Color['RED']
      <Color.RED: 1>
    
    Enumerations can be iterated over, and know how many members they have:
    
    >>> len(Color)
    3
    
    >>> list(Color)
    [<Color.RED: 1>, <Color.BLUE: 2>, <Color.GREEN: 3>]
    
    Methods can be added to enumerations, and members can have their own
    attributes -- see the documentation for details.

    ### Ancestors (in MRO)

    * enum.Enum

    ### Class variables

    `builder_preview`
    :

    `data_product_classification_configuration_update`
    :

    `data_product_classification_result_update`
    :

    `data_product_classification_update`
    :

    `data_product_create`
    :

    `data_product_data_delete`
    :

    `data_product_data_product_link`
    :

    `data_product_data_product_unlink`
    :

    `data_product_delete`
    :

    `data_product_expectations_update`
    :

    `data_product_health_check`
    :

    `data_product_info_update`
    :

    `data_product_journal_add`
    :

    `data_product_metadata_remove`
    :

    `data_product_metadata_update`
    :

    `data_product_output_link`
    :

    `data_product_output_unlink`
    :

    `data_product_profiling_update`
    :

    `data_product_publish`
    :

    `data_product_schema_update`
    :

    `data_product_spark_builder_update`
    :

    `data_product_spark_state_update`
    :

    `data_product_spark_update`
    :

    `data_product_unpublish`
    :

    `data_product_update`
    :

    `data_product_validation_update`
    :

    `data_source_connection_update`
    :

    `data_source_create`
    :

    `data_source_data_unit_link`
    :

    `data_source_data_unit_unlink`
    :

    `data_source_delete`
    :

    `data_source_health_check`
    :

    `data_source_info_update`
    :

    `data_source_journal_add`
    :

    `data_source_secret_add`
    :

    `data_source_state_update`
    :

    `data_source_update`
    :

    `data_system_create`
    :

    `data_system_data_source_link`
    :

    `data_system_data_source_unlink`
    :

    `data_system_delete`
    :

    `data_system_info_add`
    :

    `data_system_info_update`
    :

    `data_system_journal_add`
    :

    `data_system_update`
    :

    `data_unit_config_update`
    :

    `data_unit_create`
    :

    `data_unit_data_product_link`
    :

    `data_unit_data_product_unlink`
    :

    `data_unit_delete`
    :

    `data_unit_health_check`
    :

    `data_unit_info_update`
    :

    `data_unit_journal_add`
    :

    `data_unit_metadata_delete`
    :

    `data_unit_metadata_update`
    :

    `data_unit_profiling_update`
    :

    `data_unit_schema_update`
    :

    `data_unit_state_update`
    :

    `data_unit_update`
    :

    `journal_note_delete`
    :

    `journal_note_update`
    :

    `output_create`
    :

    `output_delete`
    :

    `output_info_update`
    :

    `output_journal_add`
    :

    `output_update`
    :

    `secret_add`
    :

    `secret_delete`
    :

    `secret_keys_delete`
    :

    `secret_update`
    :

    `spark_finish`
    :

    `spark_status_update`
    :

    `tag_add`
    :

    `tag_delete`
    :

`EventPacket(**data: Any)`
:   Usage docs: https://docs.pydantic.dev/2.9/concepts/models/
    
    A base class for creating Pydantic models.
    
    Attributes:
        __class_vars__: The names of the class variables defined on the model.
        __private_attributes__: Metadata about the private attributes of the model.
        __signature__: The synthesized `__init__` [`Signature`][inspect.Signature] of the model.
    
        __pydantic_complete__: Whether model building is completed, or if there are still undefined fields.
        __pydantic_core_schema__: The core schema of the model.
        __pydantic_custom_init__: Whether the model has a custom `__init__` function.
        __pydantic_decorators__: Metadata containing the decorators defined on the model.
            This replaces `Model.__validators__` and `Model.__root_validators__` from Pydantic V1.
        __pydantic_generic_metadata__: Metadata for generic models; contains data used for a similar purpose to
            __args__, __origin__, __parameters__ in typing-module generics. May eventually be replaced by these.
        __pydantic_parent_namespace__: Parent namespace of the model, used for automatic rebuilding of models.
        __pydantic_post_init__: The name of the post-init method for the model, if defined.
        __pydantic_root_model__: Whether the model is a [`RootModel`][pydantic.root_model.RootModel].
        __pydantic_serializer__: The `pydantic-core` `SchemaSerializer` used to dump instances of the model.
        __pydantic_validator__: The `pydantic-core` `SchemaValidator` used to validate instances of the model.
    
        __pydantic_extra__: A dictionary containing extra values, if [`extra`][pydantic.config.ConfigDict.extra]
            is set to `'allow'`.
        __pydantic_fields_set__: The names of fields explicitly set during instantiation.
        __pydantic_private__: Values of private attributes set on the model instance.
    
    Create a new model by parsing and validating input data from keyword arguments.
    
    Raises [`ValidationError`][pydantic_core.ValidationError] if the input data cannot be
    validated to form a valid model.
    
    `self` is explicitly positional-only to allow `self` as a field name.

    ### Ancestors (in MRO)

    * pydantic.main.BaseModel

    ### Class variables

    `message: str | dict[str, typing.Any]`
    :

    `message_type: str`
    :

    `model_computed_fields`
    :

    `model_config`
    :

    `model_fields`
    :

    `session_id: uuid.UUID | None`
    :

    `source: str`
    :

    `span_id: uuid.UUID`
    :

    `timestamp: int`
    :

    `version: str`
    :

`EventPackets(**data: Any)`
:   Usage docs: https://docs.pydantic.dev/2.9/concepts/models/
    
    A base class for creating Pydantic models.
    
    Attributes:
        __class_vars__: The names of the class variables defined on the model.
        __private_attributes__: Metadata about the private attributes of the model.
        __signature__: The synthesized `__init__` [`Signature`][inspect.Signature] of the model.
    
        __pydantic_complete__: Whether model building is completed, or if there are still undefined fields.
        __pydantic_core_schema__: The core schema of the model.
        __pydantic_custom_init__: Whether the model has a custom `__init__` function.
        __pydantic_decorators__: Metadata containing the decorators defined on the model.
            This replaces `Model.__validators__` and `Model.__root_validators__` from Pydantic V1.
        __pydantic_generic_metadata__: Metadata for generic models; contains data used for a similar purpose to
            __args__, __origin__, __parameters__ in typing-module generics. May eventually be replaced by these.
        __pydantic_parent_namespace__: Parent namespace of the model, used for automatic rebuilding of models.
        __pydantic_post_init__: The name of the post-init method for the model, if defined.
        __pydantic_root_model__: Whether the model is a [`RootModel`][pydantic.root_model.RootModel].
        __pydantic_serializer__: The `pydantic-core` `SchemaSerializer` used to dump instances of the model.
        __pydantic_validator__: The `pydantic-core` `SchemaValidator` used to validate instances of the model.
    
        __pydantic_extra__: A dictionary containing extra values, if [`extra`][pydantic.config.ConfigDict.extra]
            is set to `'allow'`.
        __pydantic_fields_set__: The names of fields explicitly set during instantiation.
        __pydantic_private__: Values of private attributes set on the model instance.
    
    Create a new model by parsing and validating input data from keyword arguments.
    
    Raises [`ValidationError`][pydantic_core.ValidationError] if the input data cannot be
    validated to form a valid model.
    
    `self` is explicitly positional-only to allow `self` as a field name.

    ### Ancestors (in MRO)

    * pydantic.main.BaseModel

    ### Class variables

    `model_computed_fields`
    :

    `model_config`
    :

    `model_fields`
    :

    `packets: list[neos_common.event.EventPacket]`
    :

`EventScope(*args, **kwds)`
:   Create a collection of name/value pairs.
    
    Example enumeration:
    
    >>> class Color(Enum):
    ...     RED = 1
    ...     BLUE = 2
    ...     GREEN = 3
    
    Access them by:
    
    - attribute access:
    
      >>> Color.RED
      <Color.RED: 1>
    
    - value lookup:
    
      >>> Color(1)
      <Color.RED: 1>
    
    - name lookup:
    
      >>> Color['RED']
      <Color.RED: 1>
    
    Enumerations can be iterated over, and know how many members they have:
    
    >>> len(Color)
    3
    
    >>> list(Color)
    [<Color.RED: 1>, <Color.BLUE: 2>, <Color.GREEN: 3>]
    
    Methods can be added to enumerations, and members can have their own
    attributes -- see the documentation for details.

    ### Ancestors (in MRO)

    * enum.Enum

    ### Class variables

    `builder`
    :

    `data_product`
    :

    `data_product_classification`
    :

    `data_product_classification_configuration`
    :

    `data_product_classification_result`
    :

    `data_product_data`
    :

    `data_product_data_product`
    :

    `data_product_data_quality`
    :

    `data_product_expectations`
    :

    `data_product_health`
    :

    `data_product_info`
    :

    `data_product_journal`
    :

    `data_product_metadata`
    :

    `data_product_output`
    :

    `data_product_profiling`
    :

    `data_product_schema`
    :

    `data_product_spark`
    :

    `data_product_spark_builder`
    :

    `data_product_spark_state`
    :

    `data_product_validation`
    :

    `data_source`
    :

    `data_source_connection`
    :

    `data_source_data_unit`
    :

    `data_source_health`
    :

    `data_source_info`
    :

    `data_source_journal`
    :

    `data_source_secret`
    :

    `data_source_state`
    :

    `data_system`
    :

    `data_system_data_source`
    :

    `data_system_info`
    :

    `data_system_journal`
    :

    `data_unit`
    :

    `data_unit_config`
    :

    `data_unit_data_product`
    :

    `data_unit_health`
    :

    `data_unit_info`
    :

    `data_unit_journal`
    :

    `data_unit_metadata`
    :

    `data_unit_profiling`
    :

    `data_unit_schema`
    :

    `data_unit_state`
    :

    `journal_note`
    :

    `output`
    :

    `output_info`
    :

    `output_journal`
    :

    `secret`
    :

    `secret_keys`
    :

    `spark`
    :

    `spark_status`
    :

    `tag`
    :

`EventType(*args, **kwds)`
:   Create a collection of name/value pairs.
    
    Example enumeration:
    
    >>> class Color(Enum):
    ...     RED = 1
    ...     BLUE = 2
    ...     GREEN = 3
    
    Access them by:
    
    - attribute access:
    
      >>> Color.RED
      <Color.RED: 1>
    
    - value lookup:
    
      >>> Color(1)
      <Color.RED: 1>
    
    - name lookup:
    
      >>> Color['RED']
      <Color.RED: 1>
    
    Enumerations can be iterated over, and know how many members they have:
    
    >>> len(Color)
    3
    
    >>> list(Color)
    [<Color.RED: 1>, <Color.BLUE: 2>, <Color.GREEN: 3>]
    
    Methods can be added to enumerations, and members can have their own
    attributes -- see the documentation for details.

    ### Ancestors (in MRO)

    * enum.Enum

    ### Class variables

    `builder`
    :

    `data_product`
    :

    `data_source`
    :

    `data_system`
    :

    `data_unit`
    :

    `journal_note`
    :

    `output`
    :

    `secret`
    :

    `spark`
    :

    `tag`
    :

`EventVersion(major: int, minor: int, patch: int)`
:   Define version of the event.
    
    Args:
        major (int): version of the Gateway API
        minor (int): breaking changes
        patch (int): non-breaking changes

    ### Class variables

    `VERSION_PATTERN`
    :

    ### Static methods

    `from_string(value: str) ‑> neos_common.event.EventVersion`
    :

`ProfilingResult(**data: Any)`
:   Profiling results model.
    
    Create a new model by parsing and validating input data from keyword arguments.
    
    Raises [`ValidationError`][pydantic_core.ValidationError] if the input data cannot be
    validated to form a valid model.
    
    `self` is explicitly positional-only to allow `self` as a field name.

    ### Ancestors (in MRO)

    * pydantic.main.BaseModel

    ### Class variables

    `column_count: int`
    :

    `column_stats: list[dict] | dict[str, typing.Any]`
    :

    `created_at: datetime.datetime`
    :

    `dataset_type: str`
    :

    `entity_identifier: uuid.UUID`
    :

    `id_: uuid.UUID`
    :

    `model_computed_fields`
    :

    `model_config`
    :

    `model_fields`
    :

    `profile_sample: float`
    :

    `row_count: int`
    :

`SyncEmitter()`
:   Helper class that provides a standard way to create an ABC using
    inheritance.

    ### Ancestors (in MRO)

    * abc.ABC

    ### Methods

    `emit(self, event_packet: neos_common.event.EventPacket) ‑> None`
    :

`SyncEvent(emitter: neos_common.event.SyncEmitter, source: str = 'source')`
:   Helper class that provides a standard way to create an ABC using
    inheritance.

    ### Ancestors (in MRO)

    * abc.ABC

    ### Methods

    `emit(self, message: str, span_id: Optional[Annotated[uuid.UUID, UuidVersion(uuid_version=4), PlainSerializer(func=<function <lambda> at 0x76475c731b20>, return_type=PydanticUndefined, when_used='always')]] = None, message_type: str = 'unknown') ‑> uuid.UUID`
    :

    `version(self) ‑> neos_common.event.EventVersion`
    :

`TmpEmitter(max_emit_log_line_length: int = 1000)`
:   Helper class that provides a standard way to create an ABC using
    inheritance.

    ### Ancestors (in MRO)

    * neos_common.event.Emitter
    * abc.ABC

    ### Static methods

    `ensure_root_folder_exists() ‑> pathlib.Path`
    :

    `split_uuid_to_dirs_and_filename(span_id: uuid.UUID) ‑> tuple[str, str, str]`
    :   Split span_id (uuid) into nested directories.
        
        Helper function that splits span_id (uuid) into nested directories.
        
        span_dir  span_subdir  span_filename
           87   /      39    / 0265-e23d-4574-b71e-dd1d61a74496
        
        for the purpose of storing large amount of files and maintaining performance
        with filesystems and other os tools
        
        Args:
        ----
        span_id: uuid.uuid4
        
        Returns: tuple (span_dir, span_subdir, span_filename)

    ### Methods

    `clear_oldest_span_id_event(self, span_id: Annotated[uuid.UUID, UuidVersion(uuid_version=4), PlainSerializer(func=<function <lambda> at 0x76475c731b20>, return_type=PydanticUndefined, when_used='always')], session_id: Optional[Annotated[uuid.UUID, UuidVersion(uuid_version=4), PlainSerializer(func=<function <lambda> at 0x76475c731b20>, return_type=PydanticUndefined, when_used='always')]] = None) ‑> None`
    :

    `emit(self, event_packet: neos_common.event.EventPacket) ‑> None`
    :

    `ensure_emit_log_keep_size(self) ‑> None`
    :

    `get_event_filepath(self, span_id: uuid.UUID, session_id: uuid.UUID | None = None) ‑> pathlib.Path`
    :   Generate the file path for the emitted event.
        
        Args:
            span_id (uuid.UUID): The UUID for the event span.
            session_id (typing.Optional[str], optional): The user session ID,
            if applicable. Defaults to None.
        
        Returns:
            Path: The file path where the emitted event is saved.

    `read_event_packets(self, span_id: uuid.UUID, session_id: uuid.UUID | None = None) ‑> neos_common.event.EventPackets`
    :   Read event packets from a given file path.
        
        Args:
            span_id (uuid.UUID): The UUID for the event span.
            session_id (typing.Optional[str], optional): The user session ID, if applicable.
            Defaults to None.
        
        Returns:
            EventPackets: The event packets read from the file.

    `save_event_packets(self, span_id: Annotated[uuid.UUID, UuidVersion(uuid_version=4), PlainSerializer(func=<function <lambda> at 0x76475c731b20>, return_type=PydanticUndefined, when_used='always')], event_packets: neos_common.event.EventPackets, session_id: Optional[Annotated[uuid.UUID, UuidVersion(uuid_version=4), PlainSerializer(func=<function <lambda> at 0x76475c731b20>, return_type=PydanticUndefined, when_used='always')]] = None) ‑> None`
    :   Save event packets with the given span ID and optional session ID.
        
        Args:
            span_id (UUID4): Unique identifier for the span of the event.
            event_packets (EventPackets): The event packets to be saved.
            session_id (UUID4 | None, optional): Optional session ID. Defaults to None.

    `update_emit_log(self, event_packet: neos_common.event.EventPacket) ‑> None`
    :

`ValidationResult(**data: Any)`
:   Data Quality validation results model.
    
    Create a new model by parsing and validating input data from keyword arguments.
    
    Raises [`ValidationError`][pydantic_core.ValidationError] if the input data cannot be
    validated to form a valid model.
    
    `self` is explicitly positional-only to allow `self` as a field name.

    ### Ancestors (in MRO)

    * pydantic.main.BaseModel

    ### Class variables

    `category_weights: dict`
    :

    `column_score: dict[str, int]`
    :

    `column_stats: dict`
    :

    `entity_identifier: uuid.UUID`
    :

    `expectations_id: uuid.UUID`
    :

    `field_thresholds: dict`
    :

    `global_stats: dict`
    :

    `id_: uuid.UUID`
    :

    `model_computed_fields`
    :

    `model_config`
    :

    `model_fields`
    :

    `raw_result: dict`
    :

    `score: int`
    :

    `success: bool`
    :

    `success_percentage: float`
    :

    `table_stats: dict`
    :

    `threshold: float`
    :