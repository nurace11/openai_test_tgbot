from aiogram import Bot, Dispatcher
import configparser
import openai
from aiogram.contrib.fsm_storage.memory import MemoryStorage

config = configparser.ConfigParser()
config.read('resources/application.ini')

storage = MemoryStorage()

openai.api_key = config['OPEN_AI']['KEY']
admins_ids = config['BOT']['OWNER_ID'].split(',')
bot = Bot(token= config['BOT']['TOKEN'])
dp = Dispatcher(bot, storage=storage)

usersDatabase = set()
