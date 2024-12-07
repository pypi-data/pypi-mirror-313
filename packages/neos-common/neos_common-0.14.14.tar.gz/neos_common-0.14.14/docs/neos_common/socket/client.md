Module neos_common.socket.client
================================

Classes
-------

`AsyncTCPClient(host: str, port: int, encoder: type[json.encoder.JSONEncoder] | None = None)`
:   Base implementation for asyncio stream socket service client.
    
    TCPClient instantiator.
    
    Args:
    ----
    host: socket service host name
    port: socket service port
    encoder: json encoder for request messages

    ### Methods

    `send_request(self, request: dict) ‑> dict`
    :   Send a request to socket service.
        
        Handle socket connection errors, and response timeouts.

`TCPClient(host: str, port: int, timeout: int = 10, wait: int = 10, encoder: type[json.encoder.JSONEncoder] | None = None)`
:   Base implementation for socket service client.
    
    TCPClient instantiator.
    
    Args:
    ----
    host: socket service host name
    port: socket service port
    timeout: number of seconds to wait for a connection
    wait: number of seconds to wait for a response from service
    encoder: json encoder for request messages

    ### Methods

    `send_request(self, request: dict) ‑> dict`
    :   Send a request to socket service.
        
        Handle socket connection errors, and response timeouts.