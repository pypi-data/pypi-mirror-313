from neos_common.error import UnauthorisedError


class TestError(UnauthorisedError):
    message_ = "Test error."
    reason_ = "test-error"


class NoCodeError(UnauthorisedError):
    title = "Test error."

    @property
    def type(self):
        return "no-code"
