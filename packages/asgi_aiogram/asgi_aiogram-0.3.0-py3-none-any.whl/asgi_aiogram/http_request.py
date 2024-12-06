from typing import Callable, TypeVar, Union

from asgi_aiogram.aliases import Receiver, Sender
from asgi_aiogram.asgi import read_body
from asgi_aiogram.strategy import BaseStrategy
from asgi_aiogram.types import ScopeType

NO_HEADER = object()
T = TypeVar('T')

class Headers:
    def __init__(self, scope: ScopeType):
        self.scope = scope
        self._chance_one: dict[str, Union[str, NO_HEADER]] = {}
        self._chance_all: dict[str, list[str]] = {}

    def _get_one(self, key: str | bytes) -> Union[str, NO_HEADER]:
        if key not in self._chance_one:
            if isinstance(key, str):
                b_key = key.encode()
            else:
                b_key = key
            for h_name, h_value in self.scope["headers"]:
                if h_name == b_key:
                    self._chance_one[key] = h_value.decode()
                    break
            self._chance_one[key] = NO_HEADER
        return self._chance_one[key]

    def _get_all(self, key: str | bytes) -> list[str]:
        if key not in self._chance_all:
            self._chance_all[key] = items = []
            if isinstance(key, str):
                b_key = key.encode()
            else:
                b_key = key
            for h_name, h_value in self.scope["headers"]:
                if h_name == b_key:
                    items.append(h_value.decode())
        return self._chance_all[key]

    def __getitem__(self, key: str):
        header = self._get_one(key=key)
        if header is NO_HEADER:
            raise KeyError(key)
        return header

    def get(self, key: str | bytes, default: T = None) -> str | T:
        header = self._get_one(key=key)
        if header is NO_HEADER:
            return default
        return header

    def get_all(self, key: str | bytes) -> list[str] | list[str]:
        return self._get_all(key=key)

    def __setitem__(self, key, value):
        raise Exception("Readonly")

    @property
    def raw(self):
        return self.scope["headers"]



class Request:
    def __init__(self, scope: ScopeType, receive: Receiver, send: Sender, strategy: BaseStrategy):
        self._scope = scope
        self._receive = receive
        self._send = send
        self._strategy = strategy
        self._body = None
        self._json = None
        self._text = None
        self._headers = None

    async def body(self) -> bytes:
        if self._body is None:
            self._body = await read_body(self._receive)
        return self._body

    async def json(self, loads: Callable | None = None) -> dict:
        if self._json is None:
            loads = loads or self._strategy.loads
            self._json = loads(await self.body())
        return self._json

    async def text(self, encoding: str = "utf-8") -> str:
        if self._text is None:
            self._text = (await self.body()).decode(encoding=encoding)
        return self._text

    @property
    def headers(self) -> Headers:
        if self._headers is None:
            self._headers = Headers(self._scope)
        return self._headers

