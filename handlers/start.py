import asyncio

from aiogram import F, Router
from aiogram.filters import Command, StateFilter
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup

from interface.button_keyboard import *
from interface.inline_keyboard import *
from interface.templates import *
from interface.callback_classes import *

start_router = Router()

@start_router.message(Command("start"))
async def start(message: Message):
    kb = await buildInlineKB(["Найти работу", "Найти работника"], ["worker", "employer"])
    await message.answer("Привет, мы поможем тебе найти работу или работника, но для начала выбери, что тебе нужно", reply_markup=kb)
    