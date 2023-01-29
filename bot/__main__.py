import asyncio
import configparser

from aiogram import Bot, Dispatcher, executor

from db import get_session_maker, create_async_engine, proceed_schemas, BaseModel

config = configparser.ConfigParser()
config.read('resources/application.ini')

global dp


async def main() -> None:
    bot = Bot(token=config['BOT']['TOKEN'])
    dp:Dispatcher = Dispatcher(bot)

    postgres_url = "postgresql+asyncpg://postgres:postgres@localhost:5432/aiogram_tg_test"

    async_engine = create_async_engine(postgres_url)

    session_maker = get_session_maker(async_engine)
    await proceed_schemas(async_engine, BaseModel.metadata)

    dp.data['session_maker'] = session_maker

    await dp.start_polling()


if __name__ == '__main__':
    asyncio.run(main())
