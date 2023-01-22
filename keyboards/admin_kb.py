from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Admin buttons
button_load = KeyboardButton('/load')
button_delete = KeyboardButton('/delete')

button_case_admin = ReplyKeyboardMarkup(resize_keyboard=True)\
    .add(button_load)\
    .add(button_delete)