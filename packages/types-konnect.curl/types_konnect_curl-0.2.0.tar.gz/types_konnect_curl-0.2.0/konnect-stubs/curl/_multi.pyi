from ._enums import MILLISECONDS as MILLISECONDS, SECONDS as SECONDS, SocketEvt as SocketEvt, Time as Time
from ._exceptions import CurlError as CurlError
from .abc import RequestProtocol as RequestProtocol
from anyio.abc import ObjectReceiveStream as ObjectReceiveStream, ObjectSendStream as ObjectSendStream
from kodo.quantities import Quantity as Quantity
from socket import socket as Socket
from typing import Final, Self, TypeAlias, TypeVar

U = TypeVar('U')
R = TypeVar('R')
Event: TypeAlias
INFO_READ_SIZE: Final[int]

class Multi:
    def __init__(self) -> None: ...
    async def process(self, request: RequestProtocol[U, R]) -> U | R: ...

class _ExternalSocket(Socket):
    def __del__(self) -> None: ...
    @classmethod
    def from_fd(cls, fd: int, /) -> Self: ...
