import asyncio
import time
from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.filters.command import Command


from constants.option import *
from interface.button_keyboard import *
from interface.inline_keyboard import *
from interface.templates import *
from interface.callback_classes import *
from data.data_classes import *
from deepseek_core.middleware_openai import generate
from data.database import *
from interface.anketa_writedb import *
from data.temp import *
from worker import *

worker_find_router = Router()

@worker_router.message(WorkerState.find, Command("find_employer"))
async def Find(message: Message, state: FSMContext):
    await state.set_state(WorkerState.find)
    await message.answer("Начинаю поиск вакансий")
    
    worker_id = message.chat.id
    if worker_id not in workers:
        workers[worker_id] = await get_worker(worker_id)
    
    jobs = await find_best_jobs_for_worker(worker_id=worker_id, limit=100)
    tt[worker_id] = jobs
    
    if not jobs:
        await message.answer("Подходящих вакансий не найдено")
        return
    
    worker = workers[worker_id]
    skipped = set(worker.get("skipped", []))
    liked = set(worker.get("likes", []))
    
    for job in jobs:
        if job["id"] in skipped or job["id"] in liked:
            continue
            
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="👍 Лайк", callback_data=f"like_emp_{job['id']}"),
             InlineKeyboardButton(text="👎 Скип", callback_data=f"skip_emp_{job['id']}")]
        ])
        
        await message.answer(
            show_employer_profile(job),
            reply_markup=keyboard
        )
        return
    
    await message.answer("Больше подходящих вакансий нет")


@worker_router.callback_query(lambda c: c.data.startswith("like_emp_"))
async def like_employer(callback: CallbackQuery):
    worker_id = callback.message.chat.id
    employer_id = int(callback.data.split("_")[2])
    
    await add_to_worker_likes(worker_id, employer_id)
    await add_to_employer_was_likes(employer_id, worker_id)
    
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.answer("Вы лайкнули эту вакансию")

@worker_router.callback_query(lambda c: c.data.startswith("skip_emp_"))
async def skip_employer(callback: CallbackQuery):
    worker_id = callback.message.chat.id
    employer_id = int(callback.data.split("_")[2])
    
    await add_to_worker_skipped(worker_id, employer_id)
    
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.answer("Вакансия скрыта")