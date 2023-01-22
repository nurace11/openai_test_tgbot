from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from create_bot import dp, ownerTelegramId, usersDatabase
from aiogram.dispatcher.filters import Text


async def print_users_database(message: types.Message):

    if message.from_user.id == ownerTelegramId:
        text = ''
        if len(usersDatabase) == 0:
            text = 'Empty'
        for user in usersDatabase:
            text += user.__str__() + "\n\n"

        text += "\n Type /chat [telegram_user_id] to see chat history of certain user"

        await message.reply(text)


# /chat
async def print_user_chat(message: types.Message):
    if message.from_user.id == ownerTelegramId:
        if len(message.text) < 6:
            await message.reply('Type an id')
            return

        try:
            chat_id = int(message.text[len('/chat '):])
            for user in usersDatabase:
                if chat_id == user.tg_id:
                    text = f"{chat_id}, chat history: \n\n{user.chat_history}"
                    await message.reply(text)
                    return

            await message.reply('Not found')
        except ValueError as e:
            await message.reply('Enter valid id. Id contains only numbers')




class FSMAdmin(StatesGroup):
    photo = State()
    name = State()
    description = State()
    price = State()


# start of fsm dialogue
# @dp.message_handler(commands='load', state=None)
async def cm_start(message: types.Message):
    if message.from_user.id == ownerTelegramId:
        await FSMAdmin.photo.set()
        await message.reply('Send photo')


# @dp.message_handler(state='*', commands=['cancel'])
# @dp.message_handler(Text(equals='cancel', ignore_case=True), state='*')
async def cancel_adding_product_handler(message: types.Message, state: FSMContext):
    context_state = await state.get_state()
    if context_state is None:
        return
    await state.finish()
    await message.reply('OK')


# catch first answer and put it in the dictionary
# @dp.message_handler(content_types=['photo'], state=FSMAdmin.photo)
async def load_photo(message: types.Message, state: FSMContext):
    if message.from_user.id == ownerTelegramId:
        async with state.proxy() as data:
            data['photo'] = message.photo[0].file_id
        await FSMAdmin.next()
        await message.reply('Good. Now enter a name')




# @dp.message_handler(state=FSMAdmin.name)
async def load_name(message: types.Message, state: FSMContext):
    if message.from_user.id == ownerTelegramId:
        async with state.proxy() as data:
            data['name'] = message.text
        await FSMAdmin.next()
        await message.reply('nice. i need a description now')


# @dp.message_handler(state=FSMAdmin.description)
async def load_desc(message: types.Message, state: FSMContext):
    if message.from_user.id == ownerTelegramId:
        async with state.proxy() as data:
            data['description'] = message.text
        await FSMAdmin.next()
        await message.reply('awesome. send price now')


# @dp.message_handler(state=FSMAdmin.price)
async def load_price(message: types.Message, state: FSMContext):
    if message.from_user.id == ownerTelegramId:
        async with state.proxy() as data:
            data['price'] = message.text
        await message.reply('thank you')

        async with state.proxy() as data:
            await message.reply(str(data))

        await state.finish()





def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(cm_start, commands=['load'], state=None)
    dp.register_message_handler(print_users_database, commands=['database'])
    dp.register_message_handler(print_user_chat, commands=['chat'])

    dp.register_message_handler(cancel_adding_product_handler, state='*', commands='cancel')
    dp.register_message_handler(cancel_adding_product_handler, Text(equals='cancel', ignore_case=True),state='*')
    dp.register_message_handler(load_photo, content_types=['photo'], state=FSMAdmin.photo)
    dp.register_message_handler(load_name, state=FSMAdmin.name)
    dp.register_message_handler(load_desc, state=FSMAdmin.description)
    dp.register_message_handler(load_price, state=FSMAdmin.price)






