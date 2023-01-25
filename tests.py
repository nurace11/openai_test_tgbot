import openai
import configparser

#
config = configparser.ConfigParser()
config.read('resources/application.ini')
print(config['OPEN_AI']['KEY'])
print(config['BOT']['TOKEN'])

# openai.api_key = config['OPEN_AI']['KEY']
# try:
#     raise openai.error.InvalidRequestError(message='Mee', param='aa')
# except openai.error.OpenAIError as ae:
#     print('Au' + ae.user_message)

if not any(1 == u for u in [3, 4, 2, 5]):
    print("no 1")


#
# completionObj = openai.Completion()
# completionObj = completionObj.create(
#         model="text-davinci-003",
#         prompt="Hi",
#         temperature=0.5,
#         max_tokens=1000,
#         top_p=1.0,
#         frequency_penalty=0.5,
#         presence_penalty=0.0,
#         stop=["You:"]
#     )
# print(completionObj)
#
# print(completionObj.api_base_override)
# print(completionObj.api_type)
# print(completionObj.api_version)
#
# print(completionObj.api_key)
#
#
