import asyncio
import time
from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from interface.button_keyboard import *
from interface.inline_keyboard import *
from interface.templates import *
from interface.callback_classes import *
from data.data import *
from data.data_classes import *
from constant.option import sphere_option, sphere_callback
from deepseek_core.middleware_openai import generate

worker_router = Router()


@worker_router.message(WorkerState.wait)
async def flood(message:Message):
    await message.answer("Запрос генерируется.")

@worker_router.callback_query(F.data == "worker")
async def anketaStart(callback: CallbackQuery, state: FSMContext):
    await state.set_state(WorkerState.name)
    await callback.message.answer("Введите свое имя")

@worker_router.message(WorkerState.name, F.text)
async def anketaName(message: Message, state: FSMContext):
    worker_info[message.chat.id] = message.text
    print(worker_info[message.chat.id])
    await state.set_state(WorkerState.age)
    await message.answer("Введите свой возраст")

@worker_router.message(WorkerState.age, F.text)
async def anketaAge(message: Message, state: FSMContext):
    if message.text.isdigit() and 16 <= int(message.text) <= 100:
        worker_info[message.chat.id] = int(message.text)
        print(worker_info[message.chat.id])
        #await state.update_data(age=int(message.text))      !!!!!!!!!!!!!!!!!!!!!!!!!!!! возможно выход без использования СУБД, потом уточню логику работы
        await state.set_state(WorkerState.sphere)
        kb = await buildInlineKB(sphere_option, sphere_callback)
        await message.answer("Выберите свою сферу деятельности", reply_markup=kb)
    else:
        await message.answer("Пожалуйста, введите корректный возраст.")

@worker_router.callback_query(F.data.in_(sphere_callback))
async def anketasphere(callback: CallbackQuery, state: FSMContext):
    await state.update_data(sphere=callback.data)
    await callback.message.edit_text(f"Выбрано: {callback.data}")
    worker_info[callback.message.chat.id] = callback.data
    print(worker_info[callback.message.chat.id])
    time.sleep(1)
    await state.set_state(WorkerState.work_experience)
    await callback.message.answer("Укажите ваш опыт опыт работы в сфере (в годах)")

@worker_router.message(WorkerState.work_experience, F.text)
async def anketaExp(message: Message, state: FSMContext):
    if message.text.isdigit() and int(message.text) < 80:
        await state.set_state(WorkerState.about)
        await message.reply("Прекрасно! А теперь напишите пару слов о себе, о важных аспектах компании для вас, о конкретных фреймворках, языках, программах и т.д, опыт работы в которых вы имеете.")
        worker_info[message.chat.id] = int(message.text)
        print(worker_info[message.chat.id])

@worker_router.message(WorkerState.about, F.text)
async def anketaAbout(message:Message, state: FSMContext):
    await state.set_state(WorkerState.wait)
    response = await generate(message.text)
    await message.answer(response)
    await state.set_state(None)