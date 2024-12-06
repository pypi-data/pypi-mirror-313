from aiohttp.formdata import FormData

from asgi_aiogram.aliases import Sender


async def answer(send: Sender, form: FormData) -> None:
    data = form()
    body = data.decode().encode(encoding='utf-8')
    await send({
        'type': 'http.response.start',
        'status': 200,
        'headers': [
            (b'content-type', data.content_type.encode()),
            (b'content-length', str(data.size or len(body)).encode())
        ]
    })
    await send({
        'type': 'http.response.body',
        'body': body,
    })

async def _send_code(send: Sender, code: int) -> None:
    await send({
        'type': 'http.response.start',
        'status': code,
    })
    await send({
        'type': 'http.response.body',
    })

async def ok(send: Sender) -> None:
    await _send_code(send, 200)

async def error(send: Sender) -> None:
    await _send_code(send, 500)

async def not_found(send: Sender) -> None:
    await _send_code(send, 404)