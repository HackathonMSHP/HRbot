# Демо-проект к хакатону МШП 2025. Трек ChatBot.

- Команда: ... # вставьте название своей команды
- Участники: ... # вставьте имена участников

---

## Установка и запуск

1. Сделайте форк этого репозитория

2. Клонируйте репозиторий на свой компьютер:
```bash
git clone https://gitlab.informatics.ru/<...>/tg_start_project.git
cd tg_start_project
```
3. Создайте и активируйте виртуальное окружение:
```bash
# Linux/MacOS
python3 -m venv .venv
source .venv/bin/activate 

# Windows
python -m venv .venv
.\.venv\Scripts\activate
```
4. Установите зависимости:
```bash
pip install -r requirements.txt
```
5. Создайте файл `.env` и добавьте туда переменные окружения:
```bash
cp .env.example .env
# редактируем .env, добавляем наш токен
```
6. Измените main.py и создайте базу данных:
```python
await create_db()
```
7. Запишите свой токен в config.py:
8. Запустите бота:
```bash
python main.py
```
9. Вносим измененения, тестируем, разбираемся как работает код, добавляем свои функции и т.д.
```bash
git add .  # добавляем изменения в индекс
git commit -m "Описание изменений"  # фиксируем изменения
git push  # отправляем изменения на удаленный репозиторий
```

## Полезные ссылки

- [Документация SQLAlchemy](https://docs.sqlalchemy.org/en/20/)
- [Документация aiogram](https://docs.aiogram.dev/en/latest/)
- [Документация Python](https://docs.python.org/3/)