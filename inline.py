import hashlib

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import configparser

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, BotCommand
from aiogram.dispatcher.filters import Text, Command

config = configparser.ConfigParser()
config.read('resources/application.ini')

bot = Bot(token=config['BOT']['TOKEN'])
dp = Dispatcher(bot)

@dp.inline_handler()
async def inline_handler(query: types.InlineQuery):
    print("Inline from:", query.from_user.id)
    text = query.query or "echo"
    link_en = 'https://en.wikipedia.org/wiki/'+text
    link_ru = 'https://ru.wikipedia.org/wiki/'+text
    result_id: str = hashlib.md5(text.encode()).hexdigest()
    result_id_en: str = hashlib.md5(link_en.encode()).hexdigest()

    articles = [
        types.InlineQueryResultArticle(
            id=result_id,
            title='Статья Wikipedia',
            url=link_ru,
            input_message_content=types.InputTextMessageContent(message_text=link_ru)
        ),
        types.InlineQueryResultArticle(
            id=result_id_en,
            title='Wiki article en',
            url=link_en,
            input_message_content=types.InputTextMessageContent(message_text=link_en)
        )
    ]

    await query.answer(articles, cache_time=1, is_personal=True)

executor.start_polling(dp, skip_updates=True)