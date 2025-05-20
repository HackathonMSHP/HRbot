import asyncio
import time
from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters.command import Command

from interface.button_keyboard import *
from interface.inline_keyboard import *
from interface.templates import *
from interface.callback_classes import *
from data.temp import *
from data.data_classes import *

start_router = Router()

@start_router.message(Command("start"), StateFilter(None))
async def start(message: Message):
    kb = await buildInlineKB(["Создать РЕЗЮМЕ", "Создать ВАКАНСИЮ"], ["worker", "employer"])
    await message.answer("Привет, мы поможем тебе найти работу или работника, но для начала выбери, что тебе нужно", reply_markup=kb)
    