import asyncio

from aiogram import F, Router
from aiogram.filters import *
from aiogram.types import *
from aiogram.fsm.state import State, StatesGroup

from interface.button_keyboard import *
from interface.inline_keyboard import *
from interface.templates import *
from interface.callback_classes import *
from data.database import *
from data.data_classes import *

employer_router = Router()

"""@employer_router.callback_query(F.data == "Employer")
async def anketaStart(callback: CallbackQuery, state: FSMContext):
    await state.set_state(EmployerState.name_company)
    await callback.message.answer("Введите свое имя")

@employer_router.message(EmployerState.name_company, F.text)
async def anketaName(message: Message, state: FSMContext):
    employer_info[message.chat.id] = message.text
    await state.set_state(EmployerState.age)
    await message.answer("Введите свой возраст")

@employer_router.message(EmployerState.age, F.text)
async def anketaAge(message: Message, state: FSMContext):
    if message.text.isdigit() and 16 <= int(message.text) <= 100:
        employer_info[message.chat.id] = int(message.text)
        await state.set_state(EmployerState.sphere)
        kb = await buildInlineKB(sphere, sphere)
        await message.answer("Выберите свою сферу деятельности", reply_markup=kb)
    else:
        await message.answer("Пожалуйста, введите корректный возраст.")
"""