from aiogram import Router
from aiogram.types import Message

router = Router(name=__name__)


@router.message()
async def echo_handler(msg: Message) -> None:
    try:
        await msg.answer("Не понимаю, что ты хочешь от меня")
        await msg.send_copy(chat_id=msg.chat.id)
    except TypeError:
        await msg.answer("Nice try!")
