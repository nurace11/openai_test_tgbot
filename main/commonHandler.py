import os

from aiogram import types, Dispatcher
from datetime import datetime
from create_bot import bot, dp, usersInMemoryDatabase, usersRepository
import openai
from googletrans import Translator
from entity.TgUser import TgUser
from PIL import Image

# import scheduler
# import time
import uuid

translator = Translator()
tg_user: TgUser


def define_tg_user(message: types.Message):
    found: bool = False
    for user in usersInMemoryDatabase:
        if user.tg_id == message.from_user.id:
            global tg_user
            tg_user = user
            found = True
    if not found:
        tg_user = TgUser(message.from_user.id, openai.Completion(), "")
        usersRepository.add_user(tg_user)
        usersInMemoryDatabase.add(tg_user)


async def variations_dalle(message:types.Message):
    print(datetime.now(), '[VARIATIONS HANDLER] From:', message.from_user.id, 'In chat', message.chat.id, 'variations',
          message.text)

    print("[VARIATIONS]")
    await message.reply("Wait a minute...")

    last_index = len(message.photo) - 1
    consumed_photo = message.photo[last_index]
    file = await bot.get_file(consumed_photo.file_id)

    rand_img_name = str(uuid.uuid4())

    await bot.download_file(file.file_path, f'resources/images/from_tg{rand_img_name}.jpg')
    im1 = Image.open(f'resources/images/from_tg{rand_img_name}.jpg')

    if not is_square(im1):
        im1 = resize_image(im1, 1024)
    if not is_square(im1):  # delete soon
        im1 = resize_image(im1, 1024)

    # convert to png using Pillow
    im1.save(f'resources/images/test{rand_img_name}.png')

    size = "1024x1024"

    if tg_user.trial:
        response = await openai.Image.acreate_variation(
            image=open(f'resources/images/test{rand_img_name}.png', "rb"),
            n=1,
            size=size
        )
    else:
        response = await openai.Image.acreate_variation(
            api_key=tg_user.api_key,
            image=open(f'resources/images/test{rand_img_name}.png', "rb"),
            n=1,
            size=size
        )

    os.remove(f"resources/images/from_tg{rand_img_name}.jpg")
    os.remove(f'resources/images/test{rand_img_name}.png')

    await bot.send_photo(message.chat.id, photo=response['data'][0]['url'], reply_to_message_id=message.message_id)


async def generate_image_dalle_handler(message: types.Message):
    if tg_user.trial:
        response = await openai.Image.acreate(
            prompt=message.text[6:],
            n=1,
            size="1024x1024"
        )
    else:
        response = await openai.Image.acreate(
            api_key=tg_user.api_key,
            prompt=message.text[6:],
            n=1,
            size="1024x1024"
        )

    image_url = response['data'][0]['url']
    await message.reply("Wait a minute...")
    await bot.send_photo(message.chat.id, photo=image_url)


async def friend_chat_message_handler(message: types.Message):
    print(datetime.now(), '[FRIEND CHAT MESSAGE] From:', message.from_user.id, 'In chat', message.chat.id, 'text:',
          message.text)
    define_tg_user(message)

    if tg_user.auto_translate_from_user is True or tg_user.auto_translate_to_user is True:
        await friend_chat_with_translate(message)
    else:
        message_to_send = message.text

        if len(tg_user.chat_history) == 0:
            tg_user.chat_history = f"You:{message_to_send} \nFriend:"
        else:
            tg_user.chat_history = tg_user.chat_history + f"\nYou: {message_to_send} \nFriend:"

        try:
            gpt_answer = await open_ai_response(tg_user)
            await bot.send_message(message.chat.id, gpt_answer)
            tg_user.chat_history += gpt_answer
        except openai.error.OpenAIError as ae:
            await message.reply("[ERROR MESSAGE]\n\n" + ae.user_message)


async def friend_chat_with_translate(message):
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
        gpt_answer = await open_ai_response(tg_user)
        if tg_user.auto_translate_to_user is True:
            if lang != 'en' and type(lang) is not list:
                gpt_answer_to_send = translator.translate(gpt_answer, dest=lang).text
            else:
                gpt_answer_to_send = gpt_answer
        else:
            gpt_answer_to_send = gpt_answer

        await bot.send_message(message.chat.id, gpt_answer_to_send)
        tg_user.chat_history += gpt_answer

    except openai.error.OpenAIError as ae:
        await message.reply("[ERROR MESSAGE]\n\n" + ae.user_message)


async def open_ai_response(user: TgUser):
    if user.trial:
        response = await user.completion.acreate(
            model="text-davinci-003",
            prompt=user.chat_history,
            temperature=0.9,
            max_tokens=2000,
            top_p=1.0,
            frequency_penalty=0.5,
            presence_penalty=0.0,
            stop=["You:"]
        )
    else:
        response = await user.completion.acreate(
            api_key=user.api_key,
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


def resize_image(image: Image, length: int) -> Image:
    """
    Resize an image to a square. Can make an image bigger to make it fit or smaller if it doesn't fit. It also crops
    part of the image.

    :param image: Image to resize.
    :param length: Width and height of the output image.
    :return: Return the resized image.
    """
    # 1200 < 601
    if image.size[0] < image.size[1]:
        resized_image = image.resize((length, int(image.size[1] * (length / image.size[0]))))

        required_loss = (resized_image.size[1] - length)

        resized_image = resized_image.crop(
            box=(0, required_loss / 2, length, resized_image.size[1] - required_loss / 2))

        return resized_image
    else:
        resized_image = image.resize((int(image.size[0] * (length / image.size[1])), length))

        required_loss = resized_image.size[0] - length

        resized_image = resized_image.crop(
            box=(required_loss / 2, 0, resized_image.size[0] - required_loss / 2, length))

        return resized_image


def is_square(image):
    if image.width != image.height:
        return False
    return True


def register_handlers_common(dp: Dispatcher):
    dp.register_message_handler(variations_dalle, content_types=types.ContentType.PHOTO)
    dp.register_message_handler(generate_image_dalle_handler, lambda message: message.text.startswith('Image '))
    dp.register_message_handler(friend_chat_message_handler, content_types=types.ContentTypes.ANY)

