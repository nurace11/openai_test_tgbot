from aiogram import executor
from create_bot import dp
from database import sqlite_db


async def on_startup(_): # add this method in the executor.start_polling(on_startup=on_startup)
    print("Bot is online")
    sqlite_db.sql_start()


from main import adminHandler, clientHandler, commonHandler

adminHandler.register_handlers_admin(dp)
clientHandler.register_handlers_client(dp)
commonHandler.register_handlers_common(dp)

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
