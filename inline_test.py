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

# Link button
urlkb = InlineKeyboardMarkup(row_width=8) # max row width is 8, by default set to 3
urlButton1 = InlineKeyboardButton(text='Youtube', url='https://youtube.com')
urlButton2 = InlineKeyboardButton(text='Google', url='https://google.com')
x = [InlineKeyboardButton(text='aaaaaaaaaaaaaaaa', url='https://openai.com'), InlineKeyboardButton(text='bbbbbbbbbbb', url='https://coinmarketcap.com')]
urlkb\
    .insert(x[0])\
    .insert(x[1])\
    .insert(x[0])\
    .insert(x[1])\
    .insert(x[1])\
    .insert(x[1])\
    .insert(x[1])\
    .insert(x[1])\
    .insert(x[1])\
    .insert(x[1])

inkb = InlineKeyboardMarkup(row_width=2)\
    .add(InlineKeyboardButton(text='Press me', callback_data='amogus'))\
    .add(InlineKeyboardButton(text='Press me', callback_data='gamma'))

pollkb = InlineKeyboardMarkup(row_width=1)\
    .add(InlineKeyboardButton(text='Like', callback_data='like_1')) \
    .add(InlineKeyboardButton(text='Dislike', callback_data='like_0'))

polled_users_db = dict()


@dp.message_handler(commands='links')
async def ulr_command(message: types.Message):
    await message.answer('Links', reply_markup=urlkb)


@dp.message_handler(commands='tests')
async def ulr_command(message: types.Message):
    await message.answer('The required text',reply_markup=inkb)


@dp.message_handler(Command([BotCommand('poll', 'poll')]))
async def poll_command(message: types.Message):
    await message.answer('Poll', reply_markup=pollkb)


@dp.callback_query_handler(text='amogus')
async def amogus_call(callback: types.CallbackQuery):
    await callback.answer('Amogggus -_-', show_alert=True) # callback answer returns alert


@dp.callback_query_handler(text='gamma')
async def amogus_call(callback: types.CallbackQuery):
    await callback.message.answer('SODA GAMMA!!')
    await callback.answer() # end of callback (button does not loading anymore for user)


@dp.callback_query_handler(Text(startswith='like_'))
async def like_call(callback: types.CallbackQuery):
    res = callback.data.split('_')[1]

    if str(callback.from_user.id) not in polled_users_db:
        polled_users_db[f'{callback.from_user.id}'] = res
        print(polled_users_db)
        await callback.answer('Answer counted')
    else:
        await callback.answer('You have already answered', show_alert=True)




executor.start_polling(dp, skip_updates=True)


