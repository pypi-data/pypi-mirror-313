from abc import abstractmethod
from io import BytesIO
from json import dumps
from typing import Any, Callable

from asgi_aiogram.aliases import Receiver, Sender
from asgi_aiogram.types import ScopeType


def _prepare_header_value(self, value: Any) -> bytes:
    if isinstance(value, bytes):
        return value
    if isinstance(value, (list, tuple, set)):
        return b", ".join(_prepare_header_value(i) for i in value)
    return str(value).encode()


def _prepare_header_key(self, key: str) -> bytes:
    return key.lower().encode()


class HttpResponse:
    _prepare_header_value: Callable[["HttpResponse", Any], bytes] = _prepare_header_value
    _prepare_header_key: Callable[["HttpResponse", str], bytes] = _prepare_header_key
    _headers: list[tuple[bytes, bytes]]

    def _prepare_headers(self, headers: dict[str, Any]) -> list[tuple[bytes, bytes]]:
        return [
            (self._prepare_header_key(key), self._prepare_header_value(value))
            for key, value in headers.items()
        ]

    def __init__(self, status_code: int = 200, headers: dict[str, str] | None = None) -> None:
        self._status_code = status_code
        if headers is None:
            self._headers = []
        else:
            self._headers = self._prepare_headers(headers=headers)

    def add_header(self, key: bytes, value: bytes, rewrite: bool = True) -> None:
        for header_item in self._headers:
            if header_item[0] == key:
                if rewrite:
                    self._headers.remove(header_item)
                else:
                    return
        self._headers.append((key, value))

    def set_content_length(self, content_length: int | bytes, rewrite: bool = True) -> None:
        self.add_header(key=b'content-length', value=self._prepare_header_value(content_length), rewrite=rewrite)

    def set_content_type(self, content_type: str | bytes, rewrite: bool = True) -> None:
        self.add_header(key=b'content-type', value=self._prepare_header_value(content_type), rewrite=rewrite)

    @abstractmethod
    async def __call__(self, scope: ScopeType, receive: Receiver, send: Sender):
        pass


class EmptyResponse(HttpResponse):

    async def __call__(self, scope: ScopeType, receive: Receiver, send: Sender):
        await send({
            'type': 'http.response.start',
            'status': self._status_code,
            'headers': self._headers,
        })
        await send({
            'type': 'http.response.body',
        })

class BytesResponse(HttpResponse):
    async def __call__(self, scope: ScopeType, receive: Receiver, send: Sender):
        await send({
            'type': 'http.response.start',
            'status': self._status_code,
            'headers': self._headers,
        })
        while True:
            chunk = self._body.read(self._chunk_size)
            if chunk:
                await send({
                    'type': 'http.response.body',
                    'body': chunk,
                    'more_body': self._size != self._body.tell(),
                })
            break

    def __init__(
            self,
            body: bytes | BytesIO,
            chunk_size: int = 65536,
            status_code: int = 200,
            headers: dict[str, str] | None = None
    ) -> None:
        super().__init__(status_code=status_code, headers=headers)
        if isinstance(body, bytes):
            body = BytesIO(body)
        self._body = body
        self._size = body.getbuffer().nbytes
        self._chunk_size = chunk_size
        self.set_content_type(b"application/octet-stream", False)
        self.set_content_length(self._size)

class JsonResponse(BytesResponse):
    def __init__(
            self,
            body: dict | list | str | bytes,
            dumper: Callable[[str], bytes] = dumps,
            chunk_size: int = 65536,
            status_code: int = 200,
            headers: dict[str, str] | None = None
    ) -> None:
        body = dumper(body)
        if isinstance(body, str):
            body = body.encode()
        super().__init__(body=body, status_code=status_code, headers=headers, chunk_size=chunk_size)
        self.set_content_type(b"application/json")
