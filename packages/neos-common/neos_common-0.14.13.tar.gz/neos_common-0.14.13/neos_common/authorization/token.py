class TokenData:
    """Represent token data contained within a JWT."""

    def __init__(self, user_id: str, auth_token: str, resources: list[str]) -> None:
        """TokenData initiator..

        Args:
        ----
        user_id: User id.
        auth_token: Raw auth token
        resources: Optional resource urns applicable to current request.
        """
        self.user_id = user_id
        self.auth_token = auth_token
        self.resources = resources

    def get_principal(self) -> str:
        """Get principal ID from the token, usually it is the user ID."""
        return self.user_id
