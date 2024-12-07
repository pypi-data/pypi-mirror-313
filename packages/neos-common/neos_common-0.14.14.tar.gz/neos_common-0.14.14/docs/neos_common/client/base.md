Module neos_common.client.base
==============================

Functions
---------

`log_request(request: httpx.Request) ‑> None`
:   Event hook for httpx events to log requests.

Classes
-------

`Method(*args, **kwds)`
:   HTTP request methods.

    ### Ancestors (in MRO)

    * enum.Enum

    ### Class variables

    `DELETE`
    :

    `GET`
    :

    `POST`
    :

    `PUT`
    :

`NeosBearerClientAuth(token: str)`
:   

`NeosClient(*args, **kwargs)`
:   Base class for HTTP client implementations for NEOS rest services.

    ### Ancestors (in MRO)

    * typing.Protocol
    * typing.Generic

    ### Descendants

    * neos_common.client.hub_client.HubClient

    ### Class variables

    `handled_error_class`
    :   Base class for all neos exceptions.

    `unhandled_error_class`
    :   Base class for all neos exceptions.

    ### Instance variables

    `key_pair: aws4.key_pair.KeyPair | None`
    :

    `known_errors: set[str]`
    :

    `partition: str`
    :

    `service_name: str`
    :

    `token: str | None`
    :

    ### Methods

    `process_response(self, response: httpx.Response) ‑> dict`
    :