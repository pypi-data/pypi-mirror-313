from typing import Callable, Awaitable, TypeAlias

from asgi_aiogram.types import SendEventType, ReceiveEventType

Sender: TypeAlias = Callable[[SendEventType], Awaitable[None]]

Receiver: TypeAlias = Callable[[], Awaitable[ReceiveEventType]]