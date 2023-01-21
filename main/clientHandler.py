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
            user.total_tokens = 0
            user.chat_history = ''
            await message.reply("[AMOGUS INFO MESSAGE] \n\nYour chat has been cleared. Thank you")


async def command_stats(message: types.Message):
    for user in usersDatabase:
        if message.chat.id == user.tg_id:
            await message.reply("Your current completion tokens: " + str(user.total_tokens) + ". Maximum is 4000" +
                                "\n\nAll time tokens:" + str(user.all_time_tokens) +
                                "\n\n1 token ~= 4 letters or 1 token ~= 0.75 words")


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start'])
    dp.register_message_handler(command_clear, commands=['clear'])
    dp.register_message_handler(command_stats, commands=['stats'])


