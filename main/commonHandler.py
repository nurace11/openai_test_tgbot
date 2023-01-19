from aiogram import types, Dispatcher
from datetime import datetime
from create_bot import usersMessageDictionary, bot, dp, ownerTelegramId
import openai


# @dp.message_handler()
async def echo_message(message: types.Message):
    print('echo_message')
    print(datetime.now(), "[INFO] message from", message.chat.id, "message text:", message.text)
    if message.text == '/start':
        await bot.send_message(message.chat.id,
                               "Hi, nice to meet you. You will talk with chatGPT by OpenAi. Start messaging")
        usersMessageDictionary[message.chat.id] = ''

    elif message.text == '/clear_all' and message.chat.id == int(ownerTelegramId):
        openai.Completion()
        usersMessageDictionary.clear()

    else:
        if message.chat.id in usersMessageDictionary:
            usersMessageDictionary[message.chat.id] = usersMessageDictionary[message.chat.id] + "\nYou: {}".format(
                message.text) + "\nFriend:"
            print('Ok1')
        else:
            usersMessageDictionary[message.chat.id] = "You: {}".format(
                message.text) + "\nFriend:"
            print('Ok2')

        try:
            gpt_answer = open_ai_response(usersMessageDictionary[message.chat.id])
            await bot.send_message(message.chat.id, gpt_answer)
            usersMessageDictionary[message.chat.id] = usersMessageDictionary[message.chat.id] + gpt_answer
            print(usersMessageDictionary)
        except openai.OpenAIError as ae:
            await message.reply("[ERROR MESSAGE]\n\n" + ae.error)


def open_ai_response(message: str):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=message,
        temperature=0.9,
        max_tokens=2000,
        top_p=1.0,
        frequency_penalty=0.5,
        presence_penalty=0.0,
        stop=["You:"]
    )

    print(response)
    # totalTokens = int(response['usage']['total_tokens'])

    return response['choices'][0]['text']


def register_handlers_common(dp: Dispatcher):
    dp.register_message_handler(echo_message)