from aiogram import types, Dispatcher
from datetime import datetime
from create_bot import bot, dp, ownerTelegramId, usersDatabase
import openai
from googletrans import Translator
from entity.TgUser import TgUser

# import scheduler
# import time

translator = Translator()
tg_user: TgUser


def define_tg_user(message: types.Message):
    found: bool = False
    for user in usersDatabase:
        if user.tg_id == message.from_user.id:
            global tg_user
            tg_user = user
            found = True

    if not found:
        tg_user = TgUser(message.from_user.id, openai.Completion(), "")
        usersDatabase.append(tg_user)


async def friend_chat_message_handler(message: types.Message):
    print(datetime.now(), '[FRIEND CHAT MESSAGE] From:', message.from_user.id, 'In chat', message.chat.id, 'text:', message.text)
    define_tg_user(message)

    lang = translator.detect(message.text).lang
    print("Lang: ", lang)

    if lang != 'en' and type(lang) is not list:
        message_to_send = translator.translate(message.text).text
        print("[TRANSLATED] ", message_to_send)
    else:
        message_to_send = message.text

    if len(tg_user.chat_history) == 0:
        tg_user.chat_history = f"You:{message_to_send} \nFriend:"
    else:
        tg_user.chat_history = tg_user.chat_history + f"\nYou: {message_to_send} \nFriend:"

    try:
        gpt_answer = open_ai_response(tg_user)
        if lang != 'en' and type(lang) is not list:
            gpt_answer_to_send = translator.translate(gpt_answer, dest=lang).text
        else:
            gpt_answer_to_send = gpt_answer

        await bot.send_message(message.chat.id, gpt_answer_to_send)
        tg_user.chat_history += gpt_answer

    except openai.error.OpenAIError as ae:
        await message.reply("[ERROR MESSAGE]\n\n" + ae.user_message)


def open_ai_response(user: TgUser):
    response = user.completion.create(
        model="text-davinci-003",
        prompt=user.chat_history,
        temperature=0.9,
        max_tokens=2000,
        top_p=1.0,
        frequency_penalty=0.5,
        presence_penalty=0.0,
        stop=["You:"]
    )

    print(response['usage'], response['choices'][0]['text'])
    tg_user.total_tokens = int(response['usage']['total_tokens'])
    tg_user.all_time_tokens += int(response['usage']['completion_tokens'])
    return response['choices'][0]['text']


def register_handlers_common(dp: Dispatcher):
    dp.register_message_handler(friend_chat_message_handler)
