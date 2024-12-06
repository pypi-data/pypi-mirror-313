Module neos_common.socket.util
==============================

Functions
---------

`add_msg_header(msg: bytes) ‑> bytes`
:   Prepend message length header onto message.
    
    Args:
    ----
    msg: message bytestring
    
    Returns:
    -------
    new bytestring with original message length prepended.

`decode(obj: bytes | None) ‑> dict[str, typing.Any] | None`
:   Decode message received via socket.

`encode(obj: dict, encoder: type[json.encoder.JSONEncoder] | None = None) ‑> bytes`
:   JSON encode message object for sending via socket.

`len_frombytes(bmsg: bytes) ‑> int`
:   Extract length of message from a bytestring header.

`len_inbytes(msg: bytes) ‑> bytes`
:   Retrieve length of message as a bytestring.

`recv_msg(sock: socket.socket) ‑> bytearray | None`
:   Receive a message via the socket.

`recvall(sock: socket.socket, length: int) ‑> bytearray | None`
:   Get a message of a certain length from the socket stream.

`send_msg(sock: socket.socket, msg: bytes) ‑> None`
:   Send a message via the socket.

Classes
-------

`AsyncSocket(reader: asyncio.streams.StreamReader, writer: asyncio.streams.StreamWriter)`
:   

    ### Methods

    `close(self) ‑> None`
    :

    `read(self) ‑> dict | None`
    :   Receive a message via the socket.

    `write(self, msg: bytes) ‑> None`
    :   Send a message via the socket.

`SocketRequest(**data: Any)`
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

    `data: dict[str, typing.Any]`
    :

    `model_computed_fields`
    :

    `model_config`
    :

    `model_fields`
    :

    `request_type: str`
    :