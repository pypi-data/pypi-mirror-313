from typing import Sequence

from aiogram import Bot, Dispatcher

from asgi_aiogram.strategy.base import BaseBotStrategy
from asgi_aiogram.types import ScopeType


class SingleStrategy(BaseBotStrategy):
    def __init__(self, path: str, bot: Bot, dispatcher: Dispatcher):
        super().__init__()
        self._path = path
        self._bot = bot
        self.dispatcher = dispatcher

    def verify_path(self, scope: ScopeType) -> bool:
        return self._path == scope['path'] and scope["method"] == "POST"

    async def resolve_bot(self, scope: ScopeType) -> Bot | None:
        return self._bot

    async def shutdown(self, kwargs: dict):
        await super().shutdown(kwargs=kwargs)
        await self._bot.session.close()

    @property
    def bots(self) -> Sequence[Bot]:
        return [self._bot]

    @property
    def bot(self) -> Bot | None:
        return self._bot