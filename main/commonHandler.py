

from aiogram import types, Dispatcher
from datetime import datetime
from create_bot import bot, dp, ownerTelegramId, usersDatabase
import openai
from googletrans import Translator
from entity.TgUser import TgUser
from PIL import Image

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
        usersDatabase.add(tg_user)


async def friend_chat_message_handler(message: types.Message):
    print(datetime.now(), '[FRIEND CHAT MESSAGE] From:', message.from_user.id, 'In chat', message.chat.id, 'text:',
          message.text)
    define_tg_user(message)

    lang = translator.detect(message.text).lang
    print("Lang: ", lang)

    print(len(message.photo))

    # Variations
    if len(message.photo) > 0:
        print("[VARIATIONS]")
        file = await bot.get_file(message.photo[3].file_id)
        print(file, type(file))
        print(file.file_path)

        # TODO: check if photo[3] size >= 256 and make sure photo is square
        #       resize to required resolution with Pillow
        #         if message.photo[3].width / message.photo[3].height == 1:

        if (message.photo[3].width != 256 and message.photo[3].height != 256) \
                and (message.photo[3].width != 512 and message.photo[3].height != 512) \
                and (message.photo[3].width != 1024 and message.photo[3].height != 1024):
            # crop
            await message.reply("Photo must be 256x256 or 512x512 or 1024x1024 resolution, less than 4MB"
                                " and in PNG format")
            return

        await message.reply("Wait a minute...")
        if message.photo[3].height == 256:
            size = "256x256"
        elif message.photo[3].height == 512:
            size = "512x512"
        else:
            size = "1024x1024"

        await bot.download_file(file.file_path, 'resources/images/from_tg.jpg')

        # convert to png using Pillow
        im1 = Image.open(r'resources/images/from_tg.jpg')
        im1.save(r'resources/images/test.png')

        response = openai.Image.create_variation(
            image=open('resources/images/test.png', "rb"),
            n=1,
            size=size
        )

        await bot.send_photo(message.chat.id, photo=response['data'][0]['url'])
    # Generate image
    elif message.text.lower().startswith('image '):
        response = openai.Image.create(
            prompt=message.text[6:],
            n=1,
            size="1024x1024"
        )
        image_url = response['data'][0]['url']
        await message.reply("Wait a minute...")
        await bot.send_photo(message.chat.id, photo=image_url)
    else:
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
    dp.register_message_handler(friend_chat_message_handler, content_types=types.ContentTypes.ANY)
