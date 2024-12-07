Module neos_common.socket.server
================================

Classes
-------

`AsyncTCPHandler()`
:   

    ### Class variables

    `Request`
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

    ### Methods

    `setup(self) ‑> None`
    :

    `teardown(self) ‑> None`
    :

`TCPHandler(request, client_address, server)`
:   Base handler for TCP socket server.
    
    When a message is received:
        * decode it
        * format it into an instance of `cls.Request`
        * pass it to the handler defined for `request.request_type` in `cls.request_mapping`
    
    Define the mapping between Request.request_type and handlers in `cls.request_mapping`.
    Override the default SocketRequest schema via `cls.Request`

    ### Ancestors (in MRO)

    * socketserver.BaseRequestHandler

    ### Class variables

    `Request`
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

    `request_mapping: ClassVar[dict]`
    :

    ### Methods

    `handle(self) ‑> None`
    :   Handle an incoming request.
        
        Handle issues decoding, processing and validating request messages, on
        error response to the client, with error details.
        
        On success pass the validated request message to the appropriate
        handler.

`ValidationError(debug: str | None = None, reason: str | None = None, message: str | None = None, status: int | str | None = None, details: list['ErrorDict'] | None = None)`
:   Base class for all neos exceptions.
    
    Socket exception initiator.
    
    Args:
    ----
    debug: Additional context for specific error instance
    reason: error reason i.e. "neos-exception"
    status: error status i.e. "not-found"
    message: error message
    details: optional list of pydantic validation errors

    ### Ancestors (in MRO)

    * neos_common.error.NeosException
    * builtins.Exception
    * builtins.BaseException

    ### Class variables

    `status_`
    :