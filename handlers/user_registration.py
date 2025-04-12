from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove

from repositories import UserRepository, BioRepository
from utils.db_connector import async_session

router = Router(name=__name__)


class FSMRegisterUser(StatesGroup):
    waiting_for_name = State()  # ожидаем имя пользователя
    waiting_for_age = State()  # ожидаем возраст пользователя
    waiting_for_bio = State()  # ожидаем био пользователя
    registered = State()  # пользователь зарегистрирован

    # storage - pltcm мы будем хранить данные пользователя перед записью в БД
    # name: str
    # age: int
    # bio: str


# Ждем текст "Зарегистрироваться"
@router.message(
    F.text.lower().endswith("зарегистрироваться")
)  # так как добавили эмодзи
async def register(msg: Message, state: FSMContext):
    # Проверяем наличие регистрации в БД
    async with async_session() as session:
        user = await UserRepository.get_user_by_tg_id(session, msg.from_user.id)
        if user:
            await msg.answer("Ты уже зарегистрирован.")
            await state.set_state(FSMRegisterUser.registered)
        else:  # Если пользователь не зарегистрирован, то начинаем регистрацию
            # следующий шаг - ввод имени
            await msg.answer(
                "Как тебя зовут?",
                reply_markup=ReplyKeyboardRemove(
                    remove_keyboard=True
                ),  # убираем прошлую клавиатуру
            )
            # Переключаем FSMRegisterUser в waiting_for_name
            await state.set_state(FSMRegisterUser.waiting_for_name)


# Если waiting_for_name и получено новое сообщение (пользователь ввел имя)
@router.message(FSMRegisterUser.waiting_for_name)
async def process_name(msg: Message, state: FSMContext):
    # Запоминаем имя в storage
    await state.update_data(name=msg.text)
    # следующий шаг - ввод возраста
    await msg.answer(
        "Сколько тебе лет?",
        reply_markup=ReplyKeyboardRemove(remove_keyboard=True),
    )
    # Переключаем FSMRegisterUser в waiting_for_age
    await state.set_state(FSMRegisterUser.waiting_for_age)


# Если waiting_for_age и получено новое сообщение (пользователь ввел возраст)
@router.message(FSMRegisterUser.waiting_for_age)
async def process_age(msg: Message, state: FSMContext):
    # Проверяем, что возраст - число от 1 до 120
    if not msg.text.isdigit() or not 0 < int(msg.text) <= 120:
        await msg.answer("Введи корректный возраст!")
        return
    # Запоминаем возраст в storage
    await state.update_data(age=int(msg.text))
    # следующий шаг - ввод биографии
    await msg.answer(
        f"Отлично, {(await state.get_data())['name']}! \
        Расскажи о себе что-нибудь интересное:",
        reply_markup=ReplyKeyboardRemove(remove_keyboard=True),
    )
    # Переключаем FSMRegisterUser в waiting_for_bio
    await state.set_state(FSMRegisterUser.waiting_for_bio)


# Если waiting_for_bio и получено новое сообщение (пользователь ввел биографию)
@router.message(FSMRegisterUser.waiting_for_bio)
async def process_bio(msg: Message, state: FSMContext):
    # запоминаем биографию в storage
    await state.update_data(bio=msg.text)

    # извлекаем все данные из storage и создаем нового пользователя в БД
    data = await state.get_data()
    async with async_session() as session:
        user = await UserRepository.create_user(
            session,
            tg_username=msg.from_user.username,
            tg_id=msg.from_user.id,
        )
        await BioRepository.create_bio(
            session,
            about=f"Меня зовут {data['name']}, мне {data['age']} лет. \
            \n\n О себе: {data['bio']}",
            user_id=user.id,
        )
        await session.commit()

    await msg.answer("Ты успешно зарегистрирован!")
    # Переключаем FSMRegisterUser в registered
    await state.set_state(FSMRegisterUser.registered)


@router.message(FSMRegisterUser.registered)
async def registered(msg: Message, state: FSMContext):
    await msg.answer("Ты уже зарегистрирован.")
    await state.clear()
    await state.set_state(FSMRegisterUser.registered)
