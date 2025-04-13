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
            await message.answer("Выберите свою сферу деятельности", reply_markup=kb)
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
        "Введите опыт работы кандидата минимум и максимум через пробел в месяцах"
    )

@employer_router.message(StateFilter(EmployerState.work_experience), F.text)
async def anketaWorkExperience(message: Message, state: FSMContext):
    try:
        exp_min, exp_max = map(int, message.text.split())
        await state.update_data(
            work_experience_min=exp_min,
            work_experience_max=exp_max
        )
        await state.set_state(EmployerState.about)
        await message.answer("Введите описание вакансии")
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
            await state.clear()
        except Exception as e:
            await callback.message.answer(f"Ошибка при сохранении: {str(e)}")