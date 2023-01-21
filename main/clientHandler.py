from aiogram import types, Dispatcher
from create_bot import dp, usersDatabase
from entity.TgUser import TgUser
import openai


async def command_start(message: types.Message):
    print('[START COMMAND]')
    usersDatabase.append(TgUser(message.from_user.id, openai.Completion(), ""))


async def command_clear(message: types.Message):
    for user in usersDatabase:
        if message.chat.id == user.tg_id:
            user.completion = openai.Completion()
            user.all_time_tokens += user.completion_tokens
            user.completion_tokens = 0
            user.chat_history = ''
            await message.reply("[AMOGUS INFO MESSAGE] \n\nYour chat has been cleared. Thank you")


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start'])
    dp.register_message_handler(command_clear, commands=['clear'])


