from aiogram import Bot, Dispatcher
from aiogram import types
from aiogram import executor
from datetime import datetime
import openai
import os
import configparser

config = configparser.ConfigParser()
config.read('resources/application.ini')

openai.api_key = config['OPEN_AI']['KEY']

bot = Bot(token=config['BOT']['TOKEN'])
dp = Dispatcher(bot)

ownerTelegramId = config['BOT']['OWNER_ID']
print(ownerTelegramId)

usersMessageDictionary = {}

@dp.message_handler()
async def echo_message(message: types.Message):
    print(datetime.now(),"[INFO] message from", message.chat.id, "message text:", message.text)
    if message.text == '/start':
        await bot.send_message(message.chat.id, "Hi, nice to meet you. You will talk with chatGPT by OpenAi. Start messaging")
        usersMessageDictionary[message.chat.id] = ''

    elif message.text == '/clear':
        openai.Completion()
        usersMessageDictionary.pop(message.chat.id)
        await message.reply("[AMOGUS INFO MESSAGE] \n\nYour chat has been cleared. Thank you")
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

        gpt_answer = open_ai_response(usersMessageDictionary[message.chat.id])
        await bot.send_message(message.chat.id, gpt_answer)

        usersMessageDictionary[message.chat.id] = usersMessageDictionary[message.chat.id] + gpt_answer
        print(usersMessageDictionary)


totalTokens = 0


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
    totalTokens = int(response['usage']['total_tokens'])

    return response['choices'][0]['text']


executor.start_polling(dp, skip_updates=True)

