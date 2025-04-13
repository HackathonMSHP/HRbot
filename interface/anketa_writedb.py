from data.database import *

async def show_worker_profile(chat_id):
    worker = await get_worker(chat_id)
    if not worker:
        return "Профиль работника не найден"
    
    profile_text = (
        f"👤 <b>Профиль работника</b>\n\n"
        f"{worker.get('name', 'Не указано')}, {worker.get('age', 'Не указан')}\n"
        f"🏢 Должность: {worker.get('sphere', 'Не указана')}\n"
        f"👫 Пол: {worker.get('gender', 'Не указан')}\n"
        f"💼 Опыт работы: {worker.get('work_experience', 'Не указан')} месяцев\n"
        f"🏷️ Навыки: {', '.join(worker.get('tags', [])) if worker.get('tags') else 'Не указаны'}\n"
        f"📝 О себе: {worker.get('about', 'Не указано')}\n"
    )
    
    return profile_text

async def show_employer_profile(chat_id):
    employer = await get_employer(chat_id)
    if not employer:
        return "Профиль работодателя не найден"
    
    profile_text = (
        f"<b>Профиль работодателя</b>\n\n"
        f"{employer.get('name_company', 'Не указано')}\n"
        f"Границы возраста {employer.get('age_min', 'Не указано')}-{employer.get('age_max', 'Не указано')}\n"
        f"Сфера деятельности: {employer.get('sphere', 'Не указана')}\n"
        f"Опыт от {employer.get('work_experience_min', 'Не указано')} до {employer.get('work_experience_max', 'Не указано')} месяцев\n"
        f"Навыки: {', '.join(employer.get('need_tags', [])) if employer.get('need_tags') else 'Не указаны'}\n"
    )

    return profile_text