from aiogram import types, Dispatcher
from create_bot import dp, usersInMemoryDatabase, usersRepository, bot, admins_ids
from entity.TgUser import TgUser
from keyboards import inline_user_settings_keyobard
import openai
from database import sqlite_db


async def command_start(message: types.Message):
    print('[START COMMAND]')
    if not any(message.from_user.id == user[0] for user in usersRepository.find_all()):
        tg_user = TgUser(message.from_user.id, openai.Completion(), "")
        usersInMemoryDatabase.add(tg_user)
        usersRepository.add_user(tg_user)
        await message.answer("This bot provides access to communicate with AI ChatGPT"
                             "\n\nStart chatting by sending any message"
                             "\nSend an image to get a variation of itSend message starting with 'Image '"
                             " to make AI generate an image from text"
                             "\n/help to get available commands"
                             "\n\nDo NOT share your personal information"
                             "\n\npowered by OpenAI "
                             "\n ")
    else:
        await message.answer(
            "Welcome again"
            "\nThis bot provides access to communicate with AI ChatGPT"
            "\n\nStart chatting by sending any message"
            "\nSend an image to get a variation of itSend message starting with 'Image ' to make AI generate "
            "an image from text"
            "\n\nDo NOT share your personal information"
            "\n/help to get available commands"
            "\n\npowered by OpenAI "
        )


async def command_help(message: types.Message):
    print(f"[HELP COMMAND] {message.from_user.id}")
    text_to_send = "/clear to start a new chat with AI" \
                   "\n/stats see your statistics"

    if any(message.from_user.id == int(admin_id) for admin_id in admins_ids):
        text_to_send += "\n\nADMIN COMMANDS" \
                        "\n/database" \
                        "\n/database_ram" \
                        "\n/load" \
                        "\n/moderator"

    await message.answer(text_to_send)


async def command_clear(message: types.Message):
    print(f'[CLEAR COMMAND] {message.from_user.id}')
    for user in usersInMemoryDatabase:
        if message.chat.id == user.tg_id:
            user.completion = openai.Completion()
            usersRepository.update_user_by_id(message.chat.id, user)
            user.total_tokens = 0
            user.chat_history = ''
            await message.reply("[INFO MESSAGE] \n\nYour chat has been cleared. Thank you")


async def command_stats(message: types.Message):
    print(f"[STATS COMMAND] {message.from_user.id}")
    for user in usersInMemoryDatabase:
        if message.chat.id == user.tg_id:
            await message.reply(f"ID{message.chat.id}"
                                f"\n\nYour current completion tokens: " + str(user.total_tokens) + ". Maximum is 4000" +
                                "\n\nAll time tokens:" + str(user.all_time_tokens) +
                                "\n\n1 token ~= 4 letters or 1 token ~= 0.75 words")


@dp.message_handler(lambda message: 'taxi' in message.text)  # use Text filter instead of lambda
async def test_m(message: types.Message):
    await message.answer('taxi')


@dp.message_handler(lambda message: message.text.lower().startswith('photo'))
async def test_m(message: types.Message):
    await message.answer('photo')


async def command_menu(message: types.Message):
    print(f"[MENU COMMAND] {message.from_user.id}")
    data = await sqlite_db.sql_read()
    for product in data:  # [0] - photo, [1] - name, [2] - description, [3] - price
        print(product[0])
        await bot.send_photo(message.from_user.id, product[0],
                             f'{product[1]}\nCaption: {product[2]}\nPrice {[product[3]]}')


async def command_settings(message: types.Message):
    print("SETTINGS COMMAND ")
    user: TgUser
    for user in usersInMemoryDatabase:
        if user.tg_id == message.from_user.id:
            if user.settings_message_id is not None:
                await bot.delete_message(message.chat.id, user.settings_message_id)

            if user.auto_translate_from_user is True:
                inline_user_settings_keyobard.inline_keyboard.inline_keyboard[0][0].text = \
                    'Translate your messages for GPT-3 +'
            else:
                inline_user_settings_keyobard.inline_keyboard.inline_keyboard[0][0].text = \
                    'Translate your messages for GPT-3 -'

            if user.auto_translate_to_user is True:
                inline_user_settings_keyobard.inline_keyboard.inline_keyboard[1][0].text = \
                    'Translate messages from GPT-3  +'
            else:
                inline_user_settings_keyobard.inline_keyboard.inline_keyboard[1][0].text = \
                    'Translate messages from GPT-3  -'

            msg = await message.answer('Auto translate your messages ',
                                       reply_markup=inline_user_settings_keyobard.inline_keyboard)
            print(msg)
            user.settings_message_id = int(msg["message_id"])


@dp.callback_query_handler(lambda callback: callback.data.startswith('autoTranslate_'))
async def callback_handle(callback: types.CallbackQuery):
    print('callback received', callback)
    which = callback.data.split('_')[1]
    edit_reply_markup = callback.message.reply_markup
    user: TgUser
    for user in usersInMemoryDatabase:
        if callback.from_user.id == user.tg_id:
            print(user)
            if which == 'from':
                user.auto_translate_from_user = not user.auto_translate_from_user
                if user.auto_translate_from_user is True:
                    edit_reply_markup.inline_keyboard[0][0].text = 'Translate your messages for GPT-3 +'
                else:
                    edit_reply_markup.inline_keyboard[0][0].text = 'Translate your messages for GPT-3 -'
            else:
                user.auto_translate_to_user = not user.auto_translate_to_user
                if user.auto_translate_to_user is True:
                    edit_reply_markup.inline_keyboard[1][0].text = 'Translate messages from GPT-3  +'
                else:
                    edit_reply_markup.inline_keyboard[1][0].text = 'Translate messages from GPT-3 -'

    # todo: save auto_translate_* states in db
    await bot.edit_message_reply_markup(callback.message.chat.id, callback.message.message_id,
                                        reply_markup=edit_reply_markup)

    await callback.answer()


# @dp.message_handler(lambda message: message.text.startswith('/'))
async def non_existent_command(message: types.Message):
    await message.answer('command not found')


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start'])
    dp.register_message_handler(command_help, commands=['help'])
    dp.register_message_handler(command_clear, commands=['clear'])
    dp.register_message_handler(command_stats, commands=['stats'])
    dp.register_message_handler(command_menu, commands=['menu'])
    dp.register_message_handler(command_settings, commands=['settings'])
    dp.register_message_handler(non_existent_command, lambda message: message.text.startswith('/'))
