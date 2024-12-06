Module neos_common.error
========================

Classes
-------

`AuthorizationRequiredError(debug: str | None = None, reason: str | None = None, message: str | None = None, status: int | str | None = None, details: list['ErrorDict'] | None = None)`
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

    * neos_common.error.UnauthorisedError
    * neos_common.error.NeosException
    * builtins.Exception
    * builtins.BaseException

    ### Class variables

    `message_`
    :

`BadRequestError(debug: str | None = None, reason: str | None = None, message: str | None = None, status: int | str | None = None, details: list['ErrorDict'] | None = None)`
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

    ### Descendants

    * neos_common.error.InvalidResourceFormatError

    ### Class variables

    `status_`
    :

`ConflictError(debug: str | None = None, reason: str | None = None, message: str | None = None, status: int | str | None = None, details: list['ErrorDict'] | None = None)`
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

`ForbiddenError(debug: str | None = None, reason: str | None = None, message: str | None = None, status: int | str | None = None, details: list['ErrorDict'] | None = None)`
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

    ### Descendants

    * neos_common.error.InsufficientPermissionsError

    ### Class variables

    `status_`
    :

`IdentityAccessManagerError(debug: str | None = None, reason: str | None = None, message: str | None = None, status: int | str | None = None, details: list['ErrorDict'] | None = None)`
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

    `message_`
    :

    `reason_`
    :

`InsufficientPermissionsError(debug: str | None = None, reason: str | None = None, message: str | None = None, status: int | str | None = None, details: list['ErrorDict'] | None = None)`
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

    * neos_common.error.ForbiddenError
    * neos_common.error.NeosException
    * builtins.Exception
    * builtins.BaseException

    ### Class variables

    `message_`
    :

`InvalidAuthorizationError(debug: str | None = None, reason: str | None = None, message: str | None = None, status: int | str | None = None, details: list['ErrorDict'] | None = None)`
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

    * neos_common.error.UnauthorisedError
    * neos_common.error.NeosException
    * builtins.Exception
    * builtins.BaseException

    ### Class variables

    `message_`
    :

`InvalidResourceFormatError(debug: str | None = None, reason: str | None = None, message: str | None = None, status: int | str | None = None, details: list['ErrorDict'] | None = None)`
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

    * neos_common.error.BadRequestError
    * neos_common.error.NeosException
    * builtins.Exception
    * builtins.BaseException

    ### Class variables

    `message_`
    :

`NeosException(debug: str | None = None, reason: str | None = None, message: str | None = None, status: int | str | None = None, details: list['ErrorDict'] | None = None)`
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

    * builtins.Exception
    * builtins.BaseException

    ### Descendants

    * neos_common.error.BadRequestError
    * neos_common.error.ConflictError
    * neos_common.error.ForbiddenError
    * neos_common.error.IdentityAccessManagerError
    * neos_common.error.NotFoundError
    * neos_common.error.ServerError
    * neos_common.error.ServiceApiError
    * neos_common.error.ServiceConnectionError
    * neos_common.error.ServiceTimeoutError
    * neos_common.error.UnauthorisedError
    * neos_common.error.UnhandledServiceApiError
    * neos_common.socket.server.ValidationError

    ### Class variables

    `message_`
    :

    `reason_`
    :

    `status_`
    :

`NotFoundError(debug: str | None = None, reason: str | None = None, message: str | None = None, status: int | str | None = None, details: list['ErrorDict'] | None = None)`
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

`ServerError(debug: str | None = None, reason: str | None = None, message: str | None = None, status: int | str | None = None, details: list['ErrorDict'] | None = None)`
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

`ServiceApiError(debug: str | None = None, reason: str | None = None, message: str | None = None, status: int | str | None = None, details: list['ErrorDict'] | None = None)`
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

`ServiceConnectionError(message: str, debug: str | None = None)`
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

    `reason_`
    :

`ServiceTimeoutError(message: str, debug: str | None = None)`
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

    `reason_`
    :

`SignatureError(debug: str | None = None, reason: str | None = None, message: str | None = None, status: int | str | None = None, details: list['ErrorDict'] | None = None)`
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

    * neos_common.error.UnauthorisedError
    * neos_common.error.NeosException
    * builtins.Exception
    * builtins.BaseException

    ### Class variables

    `message_`
    :

    `reason_`
    :

`UnauthorisedError(debug: str | None = None, reason: str | None = None, message: str | None = None, status: int | str | None = None, details: list['ErrorDict'] | None = None)`
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

    ### Descendants

    * neos_common.error.AuthorizationRequiredError
    * neos_common.error.InvalidAuthorizationError
    * neos_common.error.SignatureError

    ### Class variables

    `status_`
    :

`UnhandledServiceApiError(debug: str | None = None, reason: str | None = None, message: str | None = None, status: int | str | None = None, details: list['ErrorDict'] | None = None)`
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