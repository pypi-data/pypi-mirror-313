from json import loads, dumps
from typing import Callable

from aiogram.dispatcher.event.handler import CallableObject

from asgi_aiogram.aliases import Receiver, Sender
from asgi_aiogram.http_request import Request
from asgi_aiogram.http_responses import HttpResponse
from asgi_aiogram.strategy import BaseStrategy
from asgi_aiogram.types import ScopeType


class HttpStrategy(BaseStrategy):
    kwargs: dict

    async def startup(self, kwargs: dict):
        self.kwargs = kwargs

    async def handle(self, scope: ScopeType, receive: Receiver, send: Sender) -> bytes | None:
        response = await self._handler.call(
            request=Request(scope=scope, receive=receive, send=send, strategy=self),
            **self.kwargs
        )
        if isinstance(response, HttpResponse):
            await response(scope=scope, receive=receive, send=send)
        return

    def verify_path(self, scope: ScopeType) -> bool:
        if scope["method"] != self._method:
            return False
        if scope["path"] != self._path:
            return False
        return True

    def __init__(self, method: str, path: str, handler: Callable, loads: Callable = loads, dumps: Callable = dumps):
        super().__init__(loads=loads, dumps=dumps)
        self._path = path
        self._method = method.upper()
        self._handler = CallableObject(handler)