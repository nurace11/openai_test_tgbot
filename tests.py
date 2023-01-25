import openai
import configparser

#
config = configparser.ConfigParser()
config.read('resources/application.ini')
print(config['OPEN_AI']['KEY'])
print(config['BOT']['TOKEN'])

text = None or 'echo' and 'koko' and 'lol' or '545' and None
print(0 == False)

print('5' and '5' == True)
print('4' or '2' == True)

print()

# Evaluation of Boolean expressions
# FALSE
print(bool())
print(bool(''))
print(bool([]))
print(bool(""))
print(bool(None))
print(bool(0))

print()

#
text = '' and '' or 1 and 3
print(text)

if None:
    print(None)
elif 0:
    print(0 == False)
elif -321:
    print(-321)
elif 123:
    print(123)
else:
    print('else')

print(text)

# class Amogus:
#     def __init__(self, text: str = ""):
#         self.text = text
#
#     def __str__(self):
#         return f"Amogus{id(self)} text({self.text})"
#
#     def __repr__(self):
#         return self.__str__()
#
#
# amogus = Amogus("lol")
# kamogus = [Amogus("aga"), amogus]
# print(kamogus)
#
# kamogus[0].text = '7878'
# print(kamogus)
#
# amogus.text = '9999'
# print(kamogus)
#
# amogus = Amogus('Mental Hospital')
# print(kamogus)
#
# # there is no set method like in java's ArrayList
# kamogus[1] = amogus
# print(kamogus)
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
