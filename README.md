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
6. Запустите бота:
```bash
python main.py
```
7. Вносим измененения, тестируем, разбираемся как работает код, добавляем свои функции и т.д.
```bash
git add .  # добавляем изменения в индекс
git commit -m "Описание изменений"  # фиксируем изменения
git push  # отправляем изменения на удаленный репозиторий
```

## Telegram Desktop

Можно установить Телеграм на виртуалку:
```bash
# установка
wget -O telegram.tar.xz https://telegram.org/dl/desktop/linux && tar xf telegram.tar.xz && sudo mv Telegram /opt/ && sudo ln -sf /opt/Telegram/Telegram /usr/local/bin/telegram
# запуск
telegram
```

## Полезные ссылки

- [Документация SQLAlchemy](https://docs.sqlalchemy.org/en/20/)
- [Документация aiogram](https://docs.aiogram.dev/en/latest/)
- [Документация Python](https://docs.python.org/3/)


## Проблемы

> Server certificate verification failed. CAfile: /etc/ssl/certs/ca-certificates.crt CRLfile: none

На уровне системы
```bash
git config --global http.sslverify false
```

На уровне терминала
```bash
export GIT_SSL_NO_VERIFY=1
```

## Проверка качества кода

```bash
pip install pylint
pylint --disable=C0114,R0903,C0116,C0115,R0901 **/*.py
```