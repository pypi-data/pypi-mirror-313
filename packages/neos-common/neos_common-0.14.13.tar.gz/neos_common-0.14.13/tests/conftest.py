from unittest import mock

from neos_common.authorization import base  # noqa: F401  Import so coverage picks up nocover statements


class AsyncMock(mock.MagicMock):
    def __init__(self, *args, name=None, **kwargs) -> None:
        super().__init__(name, *args, **kwargs)
        self.__str__ = mock.MagicMock(return_value=name)

    async def __call__(self, *args, **kwargs):
        return super().__call__(*args, **kwargs)
