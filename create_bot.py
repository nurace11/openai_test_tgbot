from aiogram import Bot, Dispatcher
import configparser
import openai
from aiogram.contrib.fsm_storage.memory import MemoryStorage #Store data in RAM

config = configparser.ConfigParser()
config.read('resources/application.ini')

storage = MemoryStorage()

openai.api_key = config['OPEN_AI']['KEY']
ownerTelegramId = int(config['BOT']['OWNER_ID'])
bot = Bot(token= config['BOT']['TOKEN'])
dp = Dispatcher(bot, storage=storage)

usersDatabase = list()
