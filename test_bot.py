import logging

from aiogram import Bot, Dispatcher, types, executor
import configparser
# from commands.bot_commands import bot_commands

from aiogram.types import BotCommand
from sqlalchemy import URL
import asyncpg

from db import create_async_engine, get_session_maker, proceed_schemas, BaseModel

config = configparser.ConfigParser()
config.read('resources/application.ini')

bot = Bot(token= config['BOT']['TOKEN'])
dp = Dispatcher(bot)


async def main(_) -> None:
    logging.basicConfig(level=logging.DEBUG)

    # commands_for_bot = []
    # for cmd in bot_commands:
    #     commands_for_bot.append(BotCommand(command=cmd[0], description=cmd[1])

    # postgres_url = URL.create(
    #     "postgresql:asyncpg",
    #     username="postgres",
    #     password="postgres",
    #     database="aiogram_tg_test",
    #     port=5432,
    #     host='localhost'
    # )


    postgres_url = "postgresql+asyncpg://postgres:postgres@localhost:5432/aiogram_tg_test"

    async_engine = create_async_engine(postgres_url)
    session_maker = get_session_maker(async_engine)
    await proceed_schemas(async_engine, BaseModel.metadata)


@dp.message_handler(commands=['start'])
async def new_user(message: types.Message):
    await message.answer("Hi")


executor.start_polling(dp, skip_updates=True, on_startup=main)
