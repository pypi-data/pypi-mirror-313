from neos_common.authorization import token


class TestTokenData:
    def test_init(self):
        t = token.TokenData("user-id", "auth_token", ["resource1", "resource2"])
        assert t.user_id == "user-id"
        assert t.auth_token == "auth_token"
        assert t.resources == ["resource1", "resource2"]

    def test_get_principal(self):
        t = token.TokenData("user-id", "auth_token", [])
        assert t.get_principal() == "user-id"
