from logging import getLogger
from typing import Any

from asgi_aiogram.aliases import Receiver, Sender
from asgi_aiogram.responses import not_found
from asgi_aiogram.strategy import BaseStrategy
from asgi_aiogram.types import ScopeType


class ASGIAiogram:
    def __init__(self,
        *strategies: BaseStrategy,
        **kwargs: Any
    ):
        self.strategies = strategies
        self.kwargs = kwargs
        self.logger = getLogger("asgi_aiogram")
        self.resolve_chance = {}

    def resolve_strategy(self, scope: ScopeType) -> BaseStrategy | None:
        key = (scope["method"], scope["path"])
        if key not in self.resolve_chance:
            for strategy in self.strategies:
                if strategy.verify_path(scope=scope):
                    self.resolve_chance[key] = strategy
                    return strategy
            return None
        return self.resolve_chance[key]


    async def lifespan(self, scope: ScopeType, receive: Receiver, send: Sender):
        while True:
            message = await receive()
            if message['type'] == 'lifespan.startup':
                try:
                    for strategy in self.strategies:
                        await strategy.startup(kwargs=self.kwargs)
                except Exception as e:
                    self.logger.error(e)
                    await send({'type': 'lifespan.startup.failed'})
                else:
                    await send({'type': 'lifespan.startup.complete'})
            elif message['type'] == 'lifespan.shutdown':
                try:
                    for strategy in self.strategies:
                        await strategy.shutdown(kwargs=self.kwargs)
                except Exception as e:
                    self.logger.error(e)
                    await send({'type': 'lifespan.shutdown.failed'})
                    return
                else:
                    await send({'type': 'lifespan.shutdown.complete'})
                    return

            else:
                self.logger.warning("unknown lifespan type: %s", message['type'])

    async def http(self, scope: ScopeType, receive: Receiver, send: Sender):
        strategy = self.resolve_strategy(scope=scope)
        if strategy is None:
            self.logger.warning("unknown request. method: %s path: %s", scope["method"], scope['path'])
            await not_found(send=send)
            return
        return await strategy.handle(scope=scope, receive=receive, send=send)



    async def __call__(self, scope: ScopeType, receive: Receiver, send: Sender):
        if scope['type'] == 'http':
            return await self.http(scope=scope, receive=receive, send=send)
        if scope['type'] == 'lifespan':
            return await self.lifespan(scope=scope, receive=receive, send=send)
        self.logger.warning("unsupported event type:", scope['type'])