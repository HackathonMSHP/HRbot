import asyncio
from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.types import CallbackQuery, Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from constants.option import *
from interface.inline_keyboard import buildInlineKB
from deepseek_core.middleware_openai import generate
from data.database import add_employer, get_employer
from utilities.find import *
from interface.anketa_writedb import show_worker_profile
from data.data_classes import *
from data.temp import *


employer_router = Router()
tt = {}

@employer_router.callback_query(F.data == "employer")
async def anketaStart(callback: CallbackQuery, state: FSMContext):
    await state.update_data({
        'name': None,
        'age_min': None,
        'age_max': None,
        'sphere': None,
        'work_experience_min': None,
        'work_experience_max': None,
        'about': None,
        'tags': None
    })
    await state.set_state(EmployerState.name_company)
    await callback.message.answer("Введите название компании")

@employer_router.message(StateFilter(EmployerState.name_company), F.text)
async def anketaName(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(EmployerState.age)
    await message.answer("Введите минимальный и максимальный возраст кандидата через пробел")

@employer_router.message(StateFilter(EmployerState.age), F.text)
async def anketaAge(message: Message, state: FSMContext):
    try:
        age_min, age_max = map(int, message.text.split())
        if age_min >= 16 and age_max >= age_min:
            await state.update_data(age_min=age_min, age_max=age_max)
            await state.set_state(EmployerState.sphere)
            kb = await buildInlineKB(sphere_option, sphere_callback)
            await message.answer("Выберите сферу деятельности", reply_markup=kb)
        else:
            await message.answer("Пожалуйста, введите корректный возраст (мин ≥ 16, макс ≥ мин).")
    except (ValueError, IndexError):
        await message.answer("Пожалуйста, введите два числа через пробел (мин макс).")

@employer_router.callback_query(F.data.in_(sphere_callback), StateFilter(EmployerState.sphere))
async def anketaSphere(callback: CallbackQuery, state: FSMContext):
    await state.update_data(sphere=callback.data)
    await state.set_state(EmployerState.work_experience)
    await callback.message.edit_text(
        f"Выбрано: {callback.data}\n"
        "Введите минимальный и максимальный опыт работы кандидата через пробел (в месяцах)"
    )

@employer_router.message(StateFilter(EmployerState.work_experience), F.text)
async def anketaWorkExperience(message: Message, state: FSMContext):
    try:
        exp_min, exp_max = map(int, message.text.split())
        if exp_min >= 0 and exp_max >= exp_min:
            await state.update_data(
                work_experience_min=exp_min,
                work_experience_max=exp_max
            )
            await state.set_state(EmployerState.about)
            await message.answer("Введите описание вакансии")
        else:
            await message.answer("Пожалуйста, введите корректные значения (мин ≥ 0, макс ≥ мин).")
    except (ValueError, IndexError):
        await message.answer("Пожалуйста, введите два числа через пробел (мин макс).")

@employer_router.message(StateFilter(EmployerState.about), F.text)
async def anketaAbout(message: Message, state: FSMContext):
    await state.update_data(about=message.text)
    data = await state.get_data()
    
    response = await generate(message.text)
    await state.update_data(tags=response)
    
    kb = await buildInlineKB(
        ["Попробовать снова", "Переписать текст", "Все верно"],
        ["retry", "rewrite", "continue"], 
        1
    )
    await message.answer(
        f"Мы определили нужные для вас навыки так:\n{response}\n\n"
        "Все верно?",
        reply_markup=kb
    )
    await state.set_state(EmployerState.wait)

@employer_router.callback_query(F.data.in_(["retry", "rewrite", "continue"]), StateFilter(EmployerState.wait))
async def anketaConfirm(callback: CallbackQuery, state: FSMContext):
    if callback.data == "retry":
        data = await state.get_data()
        response = await generate(data['about'])
        await state.update_data(tags=response)
        await callback.message.answer(f"Мы определили нужные для вас навыки так:\n{response}")
        
        kb = await buildInlineKB(
            ["Попробовать снова", "Переписать текст", "Все верно"],
            ["retry", "rewrite", "continue"], 
            1
        )
        await callback.message.answer("Все верно?", reply_markup=kb)
        
    elif callback.data == "rewrite":
        await state.set_state(EmployerState.about)
        await callback.message.answer("Напишите описание вакансии...")
        
    elif callback.data == "continue":
        data = await state.get_data()
        try:
            await add_employer(
                employer_id=callback.message.chat.id,
                name_company=data['name'],
                age_min=data['age_min'],
                age_max=data['age_max'],
                sphere=data['sphere'],
                gender="any",
                work_experience_min=data['work_experience_min'],
                work_experience_max=data['work_experience_max'],
                need_tags=data['tags'],
                status="find"
            )
            await callback.message.answer("Ваша анкета успешно сохранена!")
            await state.set_state(EmployerState.find)
        except Exception as e:
            await callback.message.answer(f"Ошибка при сохранении: {str(e)}")

@employer_router.message(EmployerState.find, F.text)
async def Find(message: Message, state: FSMContext):
    await state.set_state(EmployerState.find)
    await message.answer("Начинаю поиск работников")
    
    employer_id = message.chat.id
    workers_list = await find_best_workers_for_employer(employer_id, limit=10)
    tt[employer_id] = workers_list
    
    if not workers_list:
        await message.answer("Подходящих работников не найдено")
        return
    
    employer = await get_employer(employer_id)
    skipped = set(employer.get("skipped", []))
    liked = set(employer.get("likes", []))
    
    for worker in workers_list:
        if worker["id"] in skipped or worker["id"] in liked:
            continue
            
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="👍 Лайк", callback_data=f"like_wrk_{worker['id']}"),
             InlineKeyboardButton(text="👎 Скип", callback_data=f"skip_wrk_{worker['id']}")]
        ])
        
        worker_profile = await show_worker_profile(worker["id"])
        
        await message.answer(
            worker_profile,
            reply_markup=keyboard
        )
        return
    
    await message.answer("Больше подходящих работников нет")


@employer_router.callback_query(lambda c: c.data.startswith("like_wrk_"))
async def like_worker(callback: CallbackQuery):
    employer_id = callback.message.chat.id
    worker_id = int(callback.data.split("_")[2])
    
    await add_to_employer_likes(employer_id, worker_id)
    await add_to_worker_was_likes(worker_id, employer_id)
    
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.answer("Вы лайкнули этого работника")

@employer_router.callback_query(lambda c: c.data.startswith("skip_wrk_"))
async def skip_worker(callback: CallbackQuery):
    employer_id = callback.message.chat.id
    worker_id = int(callback.data.split("_")[2])
    
    await add_to_employer_skipped(employer_id, worker_id)
    
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.answer("Работник скрыт")
