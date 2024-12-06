Module neos_common.authorization.token
======================================

Classes
-------

`TokenData(user_id: str, auth_token: str, resources: list[str])`
:   Represent token data contained within a JWT.
    
    TokenData initiator..
    
    Args:
    ----
    user_id: User id.
    auth_token: Raw auth token
    resources: Optional resource urns applicable to current request.

    ### Methods

    `get_principal(self) ‑> str`
    :   Get principal ID from the token, usually it is the user ID.