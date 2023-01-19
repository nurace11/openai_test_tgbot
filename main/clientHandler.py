from aiogram import types, Dispatcher
from create_bot import dp, bot, usersMessageDictionary
import openai
from keyboards import kb_client
from aiogram.types import ReplyKeyboardRemove


# @dp.message_handler(commands=['start', 'help'])
async def command_start(message: types.Message):
    print('command handler')
    # try:
    #     await bot.send_message(message.from_user.id, 'Itadakimasu')
    #     await message.delete() # deletes message
    # except:
    #     await message.reply('Общение с ботом невозможно, активируйте его: \nhttps://t.me/amagamaAmobusBot')

    await bot.send_message(message.chat.id, 'Itadakimasu', reply_markup=kb_client)


# @dp.message_handler(commands=['clear'])
async def command_clear(message: types.Message):
    openai.Completion()
    if message.chat.id in usersMessageDictionary:
        usersMessageDictionary.pop(message.chat.id)
        await message.reply("[AMOGUS INFO MESSAGE] \n\nYour chat has been cleared. Thank you")


async def command_amonga(message: types.Message):
    await message.reply("[AMOGUS INFO MESSAGE] \n\nAmonga brother ;)", reply_markup=ReplyKeyboardRemove())


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start', 'help'])
    dp.register_message_handler(command_clear, commands=['clear'])
    dp.register_message_handler(command_amonga, commands=['amonga'])


