import asyncio
import time
from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from constants.option import *
from interface.button_keyboard import *
from interface.inline_keyboard import *
from interface.templates import *
from interface.callback_classes import *
from data.data_classes import *
from deepseek_core.middleware_openai import generate
from data.database import *

employer_router = Router()

temp = {}

@employer_router.callback_query(F.data == "employer")
async def anketaStart(callback: CallbackQuery, state: FSMContext):
    temp[callback.message.chat.id] = {}
    await state.set_state(EmployerState.name_company)
    await callback.message.answer("Введите название компании")

@employer_router.message(StateFilter(EmployerState.name_company), F.text)
async def anketaName(message: Message, state: FSMContext):
    temp[message.chat.id]["name"] = message.text
    await state.set_state(EmployerState.age)
    await message.answer("Введите минимальный и максимальный возраст кандидата через пробел")

@employer_router.message(StateFilter(EmployerState.age), F.text)
async def anketaAge(message: Message, state: FSMContext):
    if message.text.split()[0].isdigit() and message.text.split()[1].isdigit() and int(message.text.split()[0]) >= 16 and int(message.text.split()[1]) - int(message.text.split()[0]) >= 0:
        temp[message.chat.id] = list(map(int, (message.text).split()))
        await state.set_state(EmployerState.sphere)
        kb = await buildInlineKB(sphere_option, sphere_callback)
        await message.answer("Выберите свою сферу деятельности", reply_markup=kb)
    else:
        await message.answer("Пожалуйста, введите корректный возраст.")
    
@employer_router.callback_query(F.data.in_(sphere_callback), StateFilter(EmployerState.sphere))
async def anketaStart(callback: CallbackQuery, state: FSMContext):
 
    await callback.message.edit_text(f"Выбрано: {callback.data}")
    temp[callback.message.chat.id]["sphere"] = callback.data
    time.sleep(1)
    await callback.message.answer("Введите опыт работы кандидата минимум и максимум через пробел в месяцах")
    await state.set_state(EmployerState.work_experience)

    
@employer_router.message(StateFilter(EmployerState.work_experience), F.text)
async def anketaWorkExperience(message: Message, state: FSMContext):
    if message.text.split()[0].isdigit() and message.text.split()[1].isdigit():
        temp[message.chat.id]["employer_experience"] = message.text
        await state.set_state(EmployerState.about)
        await message.answer("Введите описание")
    else:
        await message.answer("Пожалуйста, введите корректный опыт работы.")
    kb = await buildInlineKB(["Попробовать снова", "Переписать текст", "Все верно"], ["retry", "rewrite", "continue"], 1)
    await message.answer("Все верно?", reply_markup=kb)

@employer_router.callback_query(F.data.in_(["retry", "rewrite", "continue"]), StateFilter(WorkerState.wait))
async def anketaFind(callback: CallbackQuery, state: FSMContext):
    if callback.data == "retry":
        response = await generate(callback.text)
        temp[callback.message.chat.id]["tags"] = response
        await callback.message.answer(f"Мы определили нужные длдя вас навыки так:\n{response}")
        kb = await buildInlineKB(["Попробывать снова", "Переписать текст", "Все верно"], ["retry", "rewrite", "continue"], 1)
        await callback.message.answer("Все верно?", reply_markup=kb)
    elif callback.data == "rewrite":
        await state.set_state(WorkerState.about)
        await callback.message.answer("Напишите пару слов о себе...")
    else:
        employer_data = temp[callback.message.chat.id]
        await add_employer(
        employer_id = callback.message.chat.id,
        name_company = employer_data["name"],
        age_min = employer_data["age"][0],
        age_max = employer_data["age"][1],
        sphere = employer_data.get("sphere", ""),
        gender = employer_data.get("gender", "any"),
        work_experience_min = int(employer_data["work_experience"].split()[0]),
        work_experience_max = int(employer_data["work_experience"].split()[1]),
        need_tags = response,
        status = "find")










