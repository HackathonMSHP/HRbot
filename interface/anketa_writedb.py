from data.database import *
from main import bot

async def show_worker_profile(chat_id):
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
    
    return profile_text

async def show_employer_profile(chat_id):
    employer = await get_employer(chat_id)
    
    profile_text = (
        f"<b>Профиль работодателя</b>\n\n"
        f"{employer['name_company']}\n"
        f"Границы возраста {employer['age_min']}-{employer['age_max']}\n"
        f"Сфера деятельности: {employer['sphere']}\n"
        f"Опыт от {employer['work_experience_min']} до {employer['work_experience_max']} месяцев\n"
        f"Навыки: {', '.join(employer['need_tags']) if employer['need_tags'] else 'Не указаны'}\n"
    )

    return profile_text