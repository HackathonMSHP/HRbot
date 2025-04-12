from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import Command
from keyboards import register_kb

router = Router(name=__name__)


@router.message(Command("start"))
async def cmd_start(msg: Message):
    await msg.answer(
        "Нажми кнопку, чтобы зарегистрироваться:", reply_markup=register_kb
    )


@router.message(Command("help"))
@router.message(F.text.lower().endswith("помощь"))
async def cmd_help(msg: Message):
    await msg.answer(
        "Я могу зарегистрировать тебя."
        "Для регистрации введи /start"
    )
