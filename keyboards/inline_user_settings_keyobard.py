from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from entity.TgUser import TgUser

inline_keyboard = InlineKeyboardMarkup()

btn_auto_translate_from_user = InlineKeyboardButton('Translate your messages for GPT-3 +',
                                                    callback_data='autoTranslate_from_toggle')
btn_auto_translate_to_user = InlineKeyboardButton('Translate messages from GPT-3  +',
                                                  callback_data='autoTranslate_to_toggle')

btn_set_api_key = InlineKeyboardButton("Set API key", callback_data='set_api_key')

inline_keyboard.row(btn_auto_translate_from_user).row(btn_auto_translate_to_user)



