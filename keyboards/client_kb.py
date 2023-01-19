from aiogram.types import ReplyKeyboardMarkup, KeyboardButton#, ReplyKeyboardRemove

b1 = KeyboardButton('/clear')
b2 = KeyboardButton('/start')
b3 = KeyboardButton('hello')
b4 = KeyboardButton('Send number', request_contact=True)
b5 = KeyboardButton('Send location', request_location=True)

kb_client = ReplyKeyboardMarkup(resize_keyboard=True)
# kb_client = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

# kb_client.add(b1).add(b2).add(b3)
# kb_client.add(b1).insert(b2).insert(b3)
kb_client.row(b1, b2, b3)\
    .row(KeyboardButton('amonga ;)'), KeyboardButton('boba ;('))\
    .row(b4, b5)
