from unittest import mock

import pytest

from neos_common.socket import util
from tests.conftest import AsyncMock

RAW_MESSAGE = b'{"hello": "world"}'
MESSAGE_HEADER = b"\x00\x00\x00\x12"


@pytest.mark.parametrize(
    ("obj", "expected"),
    [
        ({"hello": "world"}, b'{"hello": "world"}'),
    ],
)
def test_encode(obj, expected):
    r = util.encode(obj)

    assert r == expected


class UnhandledJsonObject:
    pass


def test_encode_fails_for_unhandled_object():
    with pytest.raises(TypeError):
        util.encode({"hello": UnhandledJsonObject()})


def test_decode():
    r = util.decode(RAW_MESSAGE)

    assert r == {"hello": "world"}


def test_decode_no_message():
    r = util.decode(None)

    assert r is None


def test_len_inbytes():
    assert util.len_inbytes(RAW_MESSAGE) == MESSAGE_HEADER


def test_add_msg_header():
    assert util.add_msg_header(RAW_MESSAGE) == b'\x00\x00\x00\x12{"hello": "world"}'


def test_len_frombytes():
    assert util.len_frombytes(MESSAGE_HEADER) == 18


def test_recvall():
    sock = mock.Mock()
    sock.recv.side_effect = [
        b'{"hel',  # pragma: no-spell-check
        b'lo": ',
        b'"worl',  # pragma: no-spell-check
        b'd"}',
    ]

    data = util.recvall(sock, 18)

    assert data == RAW_MESSAGE
    assert sock.recv.call_args_list == [
        mock.call(18),
        mock.call(13),
        mock.call(8),
        mock.call(3),
    ]


def test_recvall_no_data():
    sock = mock.Mock()
    sock.recv.return_value = b""

    data = util.recvall(sock, 18)

    assert data is None
    assert sock.recv.call_args == mock.call(18)


def test_recv_msg():
    sock = mock.Mock()
    sock.recv.side_effect = [
        MESSAGE_HEADER,
        b'{"hello": "world"}',
    ]

    data = util.recv_msg(sock)

    assert data == RAW_MESSAGE
    assert sock.recv.call_args_list == [
        mock.call(4),
        mock.call(18),
    ]


def test_recv_msg_no_data():
    sock = mock.Mock()
    sock.recv.side_effect = [
        b"",
    ]

    data = util.recv_msg(sock)

    assert data is None
    assert sock.recv.call_args_list == [
        mock.call(4),
    ]


def test_send_msg():
    sock = mock.Mock()

    util.send_msg(sock, RAW_MESSAGE)

    assert sock.sendall.call_args == mock.call(
        MESSAGE_HEADER + RAW_MESSAGE,
    )


class TestAsyncSocket:
    def test_write(self):
        s = util.AsyncSocket(AsyncMock(), mock.Mock())

        s.write(b"message")

        assert s.writer.write.call_args == mock.call(b"\x00\x00\x00\x07message")

    async def test_read(self):
        s = util.AsyncSocket(AsyncMock(), mock.Mock())
        s.reader.read.side_effect = [
            MESSAGE_HEADER,
            b'{"hello": "world"}',
        ]

        d = await s.read()

        assert d == {"hello": "world"}

    async def test_read_all(self):
        s = util.AsyncSocket(AsyncMock(), mock.Mock())
        s.reader.read.side_effect = [
            MESSAGE_HEADER,
            b'{"hello": "w',
            b'orld"}',
        ]

        d = await s.read()

        assert d == {"hello": "world"}
