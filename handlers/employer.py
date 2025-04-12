import asyncio

from aiogram import F, Router
from aiogram.filters import *
from aiogram.types import *
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from interface.button_keyboard import *
from interface.inline_keyboard import *
from interface.templates import *
from interface.callback_classes import *
from data.database import *
from data.data_classes import *

employer_router = Router()

temp = {}

@employer_router.callback_query(F.data == "employer")
async def anketaStart(callback: CallbackQuery, state: FSMContext):
    await state.set_state(EmployerState.name_company)
    await callback.message.answer("Введите название компании")

@employer_router.message(EmployerState.name_company, F.text)
async def anketaName(message: Message, state: FSMContext):
    temp[message.chat.id]["name"] = message.text
    await state.set_state(EmployerState.age)
    await message.answer("Введите минимальный и максимальный возраст кандидата через пробел")

@employer_router.message(EmployerState.age, F.text)
async def anketaAge(message: Message, state: FSMContext):
    if message.text.split()[0].isdigit() and message.text.split()[0].isdigit():
        temp[message.chat.id] = int(message.text)
        await state.set_state(EmployerState.sphere)
        kb = await buildInlineKB(sphere, sphere)
        await message.answer("Выберите свою сферу деятельности", reply_markup=kb)
    else:
        await message.answer("Пожалуйста, введите корректный возраст.")
    
@employer_router.callback_query(F.data.in_(sphere))
async def anketaStart(callback: CallbackQuery, state: FSMContext):
    await state.set_state(EmployerState.work_experience)
    await callback.message.answer("Введите опыт работы кандидата минимум и максимум через пробел в месяцах")

@employer_router.message(EmployerState.work_experience, F.text)
async def anketaWorkExperience(message: Message, state: FSMContext):
    if message.text.split()[0].isdigit() and message.text.split()[1].isdigit():
        temp[message.chat.id]["work_experience"] = message.text
        await state.set_state(EmployerState.about)
        await message.answer("Введите описание")
    else:
        await message.answer("Пожалуйста, введите корректный опыт работы.")

@employer_router.message(EmployerState.about, F.text)
async def anketaAbout(message: Message, state: FSMContext):
    temp[message.chat.id]["about"] = message.text
    await state.set_state(EmployerState.find)
    await message.answer("Введите хештеги кандидата через пробел")