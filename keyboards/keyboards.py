from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


register_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📝 Зарегистрироваться"),
            KeyboardButton(text="❔ Помощь"),
        ]
    ],
    resize_keyboard=True,
)  # resize_keyboard=True - кнопки будут подстраиваться под размер экрана

reply_kb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="❔ Помощь")]], resize_keyboard=True
)
