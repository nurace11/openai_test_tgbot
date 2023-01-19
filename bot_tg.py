from aiogram import Bot, Dispatcher
from aiogram import types
from aiogram import executor
import openai
import os
import configparser

config = configparser.ConfigParser()
config.read('resources/application.ini')

openai.api_key = config['OPEN_AI']['KEY']

bot = Bot(token=config['BOT']['TOKEN'])
dp = Dispatcher(bot)

usersMessageDictionary = {}

@dp.message_handler()
async def echo_message(message: types.Message):
    print("[INFO] message from", message.chat.id, "message text:", message.text)
    if message.text == '/start':
        await bot.send_message(message.chat.id, "Hi, nice to meet you. Yu will talk with chatGPT by OpenAi. Start messaging")
        usersMessageDictionary[message.chat.id] = ''
    else:
        if usersMessageDictionary[message.chat.id] != '':
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



def open_ai_response(message: str):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=message,
        temperature=0.5,
        max_tokens=1000,
        top_p=1.0,
        frequency_penalty=0.5,
        presence_penalty=0.0,
        stop=["You:"]
    )
    return response['choices'][0]['text']


executor.start_polling(dp, skip_updates=True)

