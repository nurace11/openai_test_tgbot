import logging

from aiogram import Bot, Dispatcher, types, executor
import configparser

from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession

from db import create_async_engine, get_session_maker, proceed_schemas, BaseModel, User

config = configparser.ConfigParser()
config.read('resources/application.ini')

bot = Bot(token=config['BOT']['TOKEN'])
dp = Dispatcher(bot)


async def main(_) -> None:
    logging.basicConfig(level=logging.DEBUG)
    print("Bot is online")
    await proceed_schemas(async_engine, BaseModel.metadata)


postgres_url = "postgresql+asyncpg://postgres:postgres@localhost:5432/aiogram_tg_test"
async_engine = create_async_engine(postgres_url)
session_maker = get_session_maker(async_engine)


# asyncio.run(main(7))


@dp.message_handler(commands=['start'])
async def new_user(message: types.Message):
    await message.answer("Hi")
    async with session_maker() as session:
        async with session.begin():
            session: AsyncSession
            result = await session.execute(select(User).where(User.user_id == message.from_user.id))
            result: Result
            print(result)
            db_user = result.one_or_none()

            if db_user is not None:
                pass
            else:
                ne_user = User(
                    message.from_user.id,
                    message.from_user.username
                )
                await session.merge(ne_user)
                await message.answer("You have been registered!")



#@dispatcher.update.outer_middleware()
# async def database_transaction_middleware(
#     handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
#     event: Update,
#     data: Dict[str, Any]
# ) -> Any:
#     async with database.transaction():
#         return await handler(event, data)

dp.data['session_maker'] = session_maker
executor.start_polling(dp, skip_updates=True, on_startup=main)
