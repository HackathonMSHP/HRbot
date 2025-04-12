import asyncio

from aiogram.filters import *
from aiogram.types import *
from aiogram.utils.keyboard import *

async def buildInlineKB(buttons, callbacks):
    kb = InlineKeyboardBuilder()
    for i in range(len(buttons)):
            kb.add(InlineKeyboardButton(text=buttons[i], callback_data=callbacks[i]))
    kb.adjust(3)
    return kb.as_markup() 