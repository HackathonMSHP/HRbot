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
from interface.anketa_writedb import *

worker_router = Router()
temp = {}

@worker_router.callback_query(F.data == "worker")
async def anketaStart(callback: CallbackQuery, state: FSMContext):
    await state.set_state(WorkerState.name)
    temp[callback.message.chat.id] = {}
    await callback.message.answer("Введите свое имя")

@worker_router.message(StateFilter(WorkerState.name), F.text)
async def anketaName(message: Message, state: FSMContext):
    temp[message.chat.id]["name"] = message.text
    await state.set_state(WorkerState.age)
    await message.answer("Введите свой возраст")

@worker_router.message(StateFilter(WorkerState.age), F.text)
async def anketaAge(message: Message, state: FSMContext):
    if message.text.isdigit() and 16 <= int(message.text) <= 100:
        temp[message.chat.id]["age"] = int(message.text)
        print(temp[message.chat.id])
        #await state.update_data(age=int(message.text))      !!!!!!!!!!!!!!!!!!!!!!!!!!!! возможно выход без использования СУБД, потом уточню логику работы
        await state.set_state(WorkerState.sphere)
        kb = await buildInlineKB(sphere_option, sphere_callback)
        await message.answer("Выберите свою сферу деятельности", reply_markup=kb)
    else:
        await message.answer("Пожалуйста, введите корректный возраст.")

@worker_router.callback_query(F.data.in_(sphere_callback), StateFilter(WorkerState.sphere))
async def anketasphere(callback: CallbackQuery, state: FSMContext):
    await state.update_data(sphere=callback.data)
    await callback.message.edit_text(f"Выбрано: {callback.data}")
    temp[callback.message.chat.id]["sphere"] = callback.data
    time.sleep(1)
    await state.set_state(WorkerState.work_experience)
    await callback.message.answer("Укажите ваш опыт опыт работы в сфере (в месяцах)")

@worker_router.message(WorkerState.work_experience, F.text)
async def anketaExp(message: Message, state: FSMContext):
    if message.text.isdigit():
        await state.set_state(WorkerState.about)
        await message.reply("Прекрасно! А теперь напишите пару слов о себе, о важных аспектах компании для вас, о конкретных фреймворках, языках, программах и т.д, опыт работы в которых вы имеете.")
        temp[message.chat.id]["work_experience"] = int(message.text)

@worker_router.message(WorkerState.about, F.text)
async def anketaAbout(message:Message, state: FSMContext):
    await state.set_state(WorkerState.wait)
    response = await generate(message.text)
    temp[message.chat.id]["tags"] = response
    await message.answer(f"Мы определили ваши навыки так: {response}")
    await state.set_state(WorkerState.find)
    kb = await buildInlineKB(["Сгенерировать снова", "Переписать свое резюме", "Все верно"], ["retry", "rewrite", "continue"], 1)
    await message.answer("все верно?", reply_markup=kb)

@worker_router.callback_query(F.data.in_(["retry", "rewrite", "continue"]), StateFilter(WorkerState.find))
async def anketaFind(callback: CallbackQuery, state: FSMContext):
    print(callback.data)
    if callback.data == "retry":
        response = await generate(callback.text)
        temp[callback.message.chat.id]["tags"] = response
        await callback.message.answer(f"Мы определили ваши навыки так: {response}")
        kb = await buildInlineKB(["Сгенерировать снова", "Переписать свое резюме", "Все верно"], ["retry", "rewrite", "continue"], 1)
        await callback.message.answer("все верно?", reply_markup=kb)
    elif callback.data == "rewrite":
        await state.set_state(WorkerState.about)
        await callback.message.answer("Напишите пару слов о себе...")
    else:
        worker_data = temp[callback.message.chat.id]
        
        await add_worker(
            worker_id=callback.message.chat.id,
            name=worker_data["name"],
            age=worker_data["age"],
            sphere=worker_data["sphere"],
            gender="",
            about=worker_data.get("about", ""),
            work_experience=worker_data["work_experience"],
            tags=worker_data["tags"],
            status="active"
        )
        
        await state.set_state(WorkerState.find)
        await callback.message.answer("Начинаю поиск вакансий")
        await callback.message.answer("Ваш профиль успешно сохранён!")
        await callback.message.answer(show_worker_profile(callback.message.chat.id))

