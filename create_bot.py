from aiogram import Bot, Dispatcher
import configparser
import openai
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types.bot_command import BotCommand
from repository import TgUserRepository
from entity.TgUser import TgUser

config = configparser.ConfigParser()
config.read('resources/application.ini')

storage = MemoryStorage()

openai.api_key = config['OPEN_AI']['KEY']
admins_ids = config['BOT']['OWNER_ID'].split(',')
bot = Bot(token= config['BOT']['TOKEN'])
dp = Dispatcher(bot, storage=storage)

commands = [
    BotCommand('/help', 'get all commands'),
    BotCommand('/clear', 'clears prompt. '),
    BotCommand('/stats', 'statistics'),
    BotCommand('/menu', 'db test')
]
print(commands)

admin_commands = commands.copy()
print(admin_commands)
admin_commands.extend(
    [
        BotCommand('/database', 'sqlite tg_user table'),
        BotCommand('/database_ram', 'list of users'),
        BotCommand('/load', 'final state machine (FSM) test'),
        BotCommand('/moderator', 'admin buttons test'),
    ]
)
print(admin_commands)

usersRepository = TgUserRepository
usersInMemoryDatabase = set()
