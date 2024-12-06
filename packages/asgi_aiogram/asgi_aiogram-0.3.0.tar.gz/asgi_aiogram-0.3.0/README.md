__base usage__
```python
from aiogram import Dispatcher, Bot
from asgi_aiogram import ASGIAiogram
from asgi_aiogram.strategy import SingleStrategy

dp = Dispatcher()

@dp.startup()
async def startup(dispatcher: Dispatcher, bot: Bot):
    await bot.close()
    await bot.set_webhook(
        url='https://example.com/bot',
        allowed_updates=dispatcher.resolve_used_update_types()
    )

bot = Bot(token="<token>")
app = ASGIAiogram(
    dispatcher=dp,
    strategy=SingleStrategy(bot=bot, path="/bot")
)
```

```commandline
uvicorn main:app
```
