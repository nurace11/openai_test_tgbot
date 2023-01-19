from aiogram import Bot, Dispatcher
import configparser
import openai

config = configparser.ConfigParser()
config.read('resources/application.ini')

openai.api_key = config['OPEN_AI']['KEY']
ownerTelegramId = config['BOT']['OWNER_ID']
bot = Bot(token= config['BOT']['TOKEN'])
dp = Dispatcher(bot)

usersMessageDictionary = {}
