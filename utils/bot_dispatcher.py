from aiogram import Dispatcher

import handlers as h


def create_dispatcher():
    dp = Dispatcher()
    dp.include_router(h.start)
    dp.include_router(h.user_registration)
    dp.include_router(h.echo)
    return dp
