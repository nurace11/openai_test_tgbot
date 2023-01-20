from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from create_bot import dp, bot
from aiogram.dispatcher.filters import Text

ID = None

class FSMAdmin(StatesGroup):
    photo = State()
    name = State()
    description = State()
    price = State()


#checking for admin
@dp.message_handler(commands=['moderator'], is_chat_admin=True)
async def make_changes_command(message: types.Message):
    global ID
    ID = message.from_user.id
    await bot.send_message(message.from_user.id, 'You are admin')
    await message.delete()



# start of fsm dialogue
# @dp.message_handler(commands='load', state=None)
async def cm_start(message: types.Message):
    if message.from_user.id == ID:
        await FSMAdmin.photo.set()
        await message.reply('Send photo')


# catch first answer and put it in the dictionary
# @dp.message_handler(content_types=['photo'], state=FSMAdmin.photo)
async def load_photo(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['photo'] = message.photo[0].file_id
        await FSMAdmin.next()
        await message.reply('Good. Now enter a name')


# @dp.message_handler(state=FSMAdmin.name)
async def load_name(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['name'] = message.text
        await FSMAdmin.next()
        await message.reply('nice. i need a description now')


# @dp.message_handler(state=FSMAdmin.description)
async def load_desc(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['description'] = message.text
        await FSMAdmin.next()
        await message.reply('awesome. send price now')


# @dp.message_handler(state=FSMAdmin.price)
async def load_price(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['price'] = message.text
        await message.reply('thank you')

        async with state.proxy() as data:
            await message.reply(str(data))

        await state.finish()


# @dp.message_handler(state='*', commands=['cancel'])
# @dp.message_handler(Text(equals='cancel', ignore_case=True), state='*')
async def cancel_adding_product_handler(message: types.Message, state: FSMContext):
    context_state = await state.get_state()
    if context_state is None:
        return
    await state.finish()
    await message.reply('OK')


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(cm_start, commands=['load'], state=None)

    dp.register_message_handler(load_photo, content_types=['photo'], state=FSMAdmin.photo)
    dp.register_message_handler(load_name, state=FSMAdmin.name)
    dp.register_message_handler(load_desc, state=FSMAdmin.description)
    dp.register_message_handler(load_price, state=FSMAdmin.price)

    dp.register_message_handler(cancel_adding_product_handler, state='*', commands='cancel')
    dp.register_message_handler(cancel_adding_product_handler, Text(equals='cancel', ignore_case=True),state='*')

    dp.register_message_handler(make_changes_command, commands=['moderator'], is_chat_admin=True)





