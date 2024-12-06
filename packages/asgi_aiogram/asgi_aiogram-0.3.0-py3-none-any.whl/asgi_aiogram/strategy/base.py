from abc import ABC, abstractmethod
from asyncio import Task, create_task
from collections.abc import Callable
from logging import Logger, getLogger
from typing import Sequence
from json import loads, dumps

from aiogram import Bot, Dispatcher
from aiogram.types import Update

from asgi_aiogram.aliases import Receiver, Sender
from asgi_aiogram.asgi import read_body
from asgi_aiogram.responses import not_found, error, ok
from asgi_aiogram.types import ScopeType


class BaseStrategy(ABC):
    logger: Logger
    loads: Callable = loads
    dumps: Callable = dumps

    def __init__(self, loads: Callable = loads, dumps: Callable = dumps):
        self.logger = getLogger(self.__class__.__name__)
        self.loads = loads
        self.dumps = dumps

    @abstractmethod
    def verify_path(self, scope: ScopeType) -> bool:
        pass

    async def startup(self, kwargs: dict):
        pass

    async def shutdown(self, kwargs: dict):
        pass

    @abstractmethod
    async def handle(self, scope: ScopeType, receive: Receiver, send: Sender) -> bytes | None:
        pass

class BaseBotStrategy(BaseStrategy):
    dispatcher: Dispatcher
    kwargs: dict
    task_list: set[Task]
    handle_as_tasks: bool = True

    def __init__(self, loads: Callable = loads, dumps: Callable = dumps):
        super().__init__(loads=loads, dumps=dumps)
        self.task_list = set()

    @property
    def bots(self) -> Sequence[Bot]:
        return []

    @property
    def bot(self) -> Bot | None:
        return

    async def startup(self, kwargs: dict):
        self.kwargs = kwargs
        self.kwargs.pop("bot", None)
        self.kwargs.pop("dispatcher", None)
        await self.dispatcher.emit_startup(
            **self.dispatcher.workflow_data,
            **self.kwargs,
            bots=self.bots,
            bot=self.bot,
            dispatcher=self.dispatcher,
        )

    async def shutdown(self, kwargs: dict):
        self.kwargs = kwargs
        self.kwargs.pop("bot", None)
        self.kwargs.pop("dispatcher", None)
        await self.dispatcher.emit_shutdown(
            **self.dispatcher.workflow_data,
            **self.kwargs,
            bots=self.bots,
            bot=self.bot,
            dispatcher=self.dispatcher,
        )

    @abstractmethod
    async def resolve_bot(self, scope: ScopeType) -> Bot | None:
        pass

    async def handle(self, scope: ScopeType, receive: Receiver, send: Sender) -> bytes | None:
        bot = await self.resolve_bot(scope=scope)
        if bot is None:
            self.logger.warning("unknown bot for: %s", scope['path'])
            await not_found(send=send)
            return
        try:
            cor = self.dispatcher.feed_update(
                bot=bot,
                update=Update.model_validate_json(await read_body(receive)),
                **self.kwargs,
            )
            if self.handle_as_tasks:
                handle_update_task = create_task(cor)
                self.task_list.add(handle_update_task)
                handle_update_task.add_done_callback(self.task_list.discard)
            else:
                await cor
                # if isinstance(response, TelegramMethod):
                #     form = bot.session.build_form_data(bot, response)
                #     form.add_field(
                #         name="method",
                #         value=response.__api_method__
                #     )
                #     await answer(send, form)
            await ok(send=send)
            return
        except Exception as e:
            self.logger.error(e)
            await error(send=send)
