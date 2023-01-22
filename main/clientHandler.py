from aiogram import types, Dispatcher
from create_bot import dp, usersDatabase, bot
from entity.TgUser import TgUser
import openai
from database import sqlite_db


async def command_start(message: types.Message):
    print('[START COMMAND]')
    if not any(message.from_user.id == user.tg_id for user in usersDatabase):
        usersDatabase.add(TgUser(message.from_user.id, openai.Completion(), ""))
        await message.answer("""
                             This bot provides access to communicate with AI ChatGPT
                             
                             Start chatting by sending any message
                             Send an image to get a variation of it
                             Send message starting with 'Image ' to make AI generate an image from text"
                             
                             \n\npowered by OpenAI 
        """)


async def command_clear(message: types.Message):
    print(f'[CLEAR COMMAND] {message.from_user.id}')
    for user in usersDatabase:
        if message.chat.id == user.tg_id:
            user.completion = openai.Completion()
            user.total_tokens = 0
            user.chat_history = ''
            await message.reply("[INFO MESSAGE] \n\nYour chat has been cleared. Thank you")


async def command_stats(message: types.Message):
    print(f"[STATS COMMAND] {message.from_user.id}")
    for user in usersDatabase:
        if message.chat.id == user.tg_id:
            await message.reply(f"ID{message.chat.id}"
                                f"\n\nYour current completion tokens: " + str(user.total_tokens) + ". Maximum is 4000" +
                                "\n\nAll time tokens:" + str(user.all_time_tokens) +
                                "\n\n1 token ~= 4 letters or 1 token ~= 0.75 words")


@dp.message_handler(lambda message: 'taxi' in message.text) # use Text filter instead of lambda
async def test_m(message: types.Message):
    await message.answer('taxi')


@dp.message_handler(lambda message: message.text.lower().startswith('photo'))
async def test_m(message: types.Message):
    await message.answer('photo')


async def command_menu(message: types.Message):
    data = await sqlite_db.sql_read()
    for product in data: # [0] - photo, [1] - name, [2] - description, [3] - price
        await bot.send_photo(message.from_user.id, product[0], f'{product[1]}\nCaption: {product[2]}\nPrice {[product[3]]}')


# @dp.message_handler(lambda message: message.text.startswith('/'))
async def non_existent_command(message: types.Message):
    await message.answer('command not found')


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start'])
    dp.register_message_handler(command_clear, commands=['clear'])
    dp.register_message_handler(command_stats, commands=['stats'])
    dp.register_message_handler(command_menu, commands=['menu'])
    dp.register_message_handler(non_existent_command, lambda message: message.text.startswith('/'))



