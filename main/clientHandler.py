from aiogram import types, Dispatcher
from create_bot import dp, bot, usersMessageDictionary
import openai


# @dp.message_handler(commands=['start', 'help'])
async def command_start(message: types.Message):
    print('command handler')
    # try:
    #     await bot.send_message(message.from_user.id, 'Itadakimasu')
    #     await message.delete() # deletes message
    # except:
    #     await message.reply('Общение с ботом невозможно, активируйте его: \nhttps://t.me/amagamaAmobusBot')

    await bot.send_message(message.chat.id, 'Itadakimasu')


# @dp.message_handler(commands=['clear'])
async def command_clear(message: types.Message):
    openai.Completion()
    if message.chat.id in usersMessageDictionary:
        usersMessageDictionary.pop(message.chat.id)
        await message.reply("[AMOGUS INFO MESSAGE] \n\nYour chat has been cleared. Thank you")


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start', 'help'])
    dp.register_message_handler(command_clear, commands=['clear'])


