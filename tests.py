import openai
import configparser

config = configparser.ConfigParser()
config.read('application.ini')
print(config['OPEN_AI']['KEY'])
print(config['BOT']['TOKEN'])

openai.api_key = config['OPEN_AI']['KEY']
