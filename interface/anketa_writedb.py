from data.database import *
from main import bot

async def show_worker_profile(chat_id, kb = None):
    worker = await get_worker(chat_id)
    
    profile_text = (
        f"👤 <b>Профиль работника</b>\n\n"
        f"{worker['name']}, {worker['age']}\n"
        f"🏢 Должность: {worker['sphere']}\n"
        f"👫 Пол: {worker['gender'] if worker['gender'] else 'Не указан'}\n"
        f"💼 Опыт работы: {worker['work_experience']} месяцев\n"
        f"🏷️ Навыки: {', '.join(worker['tags']) if worker['tags'] else 'Не указаны'}\n"
        f"📝 О себе: {worker['about'] if worker['about'] else 'Не указано'}\n"
    )
    
    bot.send_message(chat_id, profile_text, reply_markup=kb)

async def show_employer_profile(chat_id, kb = None):
    employer = await get_employer(chat_id)
    
    profile_text = (
        f"<b>Профиль работодателя</b>\n\n"
        f"{employer['name']}, {employer['age']}\n"
        f"Организация: {employer['organization']}\n"
        f"Сфера деятельности: {employer['sphere']}\n"
        f"Контакты: {employer['contacts']}\n"
    )

    bot.send_message(chat_id, profile_text, reply_markup=kb)