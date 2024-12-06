import asyncio
import json
import socket
import typing

import pydantic

Socket = socket.socket


class SocketRequest(pydantic.BaseModel):
    request_type: str
    data: dict[str, typing.Any]


def encode(obj: dict, encoder: type[json.JSONEncoder] | None = None) -> bytes:
    """JSON encode message object for sending via socket."""
    new = json.dumps(obj, cls=encoder)
    return new.encode()


def decode(obj: bytes | None) -> dict[str, typing.Any] | None:
    """Decode message received via socket."""
    if obj is None:
        return obj

    data: dict[str, typing.Any] = json.loads(obj.decode())
    return data


class AsyncSocket:
    def __init__(self, reader: asyncio.streams.StreamReader, writer: asyncio.streams.StreamWriter) -> None:
        self.reader = reader
        self.writer = writer

    def write(self, msg: bytes) -> None:
        """Send a message via the socket."""
        msg = add_msg_header(msg)
        self.writer.write(msg)

    async def read(self) -> dict | None:
        """Receive a message via the socket."""
        # start by getting the header
        # (which is an int of length `BYTE_COUNT`).
        # The header tells the message size in bytes.
        raw_msglen = await self.reader.read(BYTE_COUNT)
        # Then retrieve a message of length `raw_msglen`
        # this will be the actual message
        msglen = len_frombytes(raw_msglen)

        data = bytearray()
        while len(data) < msglen:
            packet = await self.reader.read(msglen - len(data))
            if not packet:
                return None
            data.extend(packet)

        return decode(data)

    def close(self) -> None:
        self.writer.close()


BYTE_COUNT = 4


def send_msg(sock: Socket, msg: bytes) -> None:
    """Send a message via the socket."""
    msg = add_msg_header(msg)
    sock.sendall(msg)


def recv_msg(sock: Socket) -> bytearray | None:
    """Receive a message via the socket."""
    # start by getting the header
    # (which is an int of length `BYTE_COUNT`).
    # The header tells the message size in bytes.
    raw_msglen = recvall(sock, BYTE_COUNT)
    if not raw_msglen:
        return None
    # Then retrieve a message of length `raw_msglen`
    # this will be the actual message
    msglen = len_frombytes(raw_msglen)
    return recvall(sock, msglen)


def recvall(sock: Socket, length: int) -> bytearray | None:
    """Get a message of a certain length from the socket stream."""
    data = bytearray()
    while len(data) < length:
        packet = sock.recv(length - len(data))
        if not packet:
            return None
        data.extend(packet)
    return data


def add_msg_header(msg: bytes) -> bytes:
    """Prepend message length header onto message.

    Args:
    ----
    msg: message bytestring

    Returns:
    -------
    new bytestring with original message length prepended.
    """
    return len_inbytes(msg) + msg


def len_inbytes(msg: bytes) -> bytes:
    """Retrieve length of message as a bytestring."""
    return len(msg).to_bytes(BYTE_COUNT, byteorder="big")


def len_frombytes(bmsg: bytes) -> int:
    """Extract length of message from a bytestring header."""
    return int.from_bytes(bmsg, byteorder="big")
