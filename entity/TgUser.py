import openai
from openai import Completion


class TgUser:
    def __init__(self, tg_id: int, completion=None, chat_history: str = None, total_tokens: int = 0,
                 all_time_tokens: int = 0, auto_translate_from_user: bool = True, auto_translate_to_user: bool = True,
                 settings_message_id: int = None, api_key: str = None, trial: bool = True):
        self.tg_id = tg_id
        self.completion = completion
        self.chat_history = chat_history
        self.total_tokens = total_tokens
        self.all_time_tokens = all_time_tokens
        self.auto_translate_from_user = auto_translate_from_user
        self.auto_translate_to_user = auto_translate_to_user
        self.settings_message_id = settings_message_id
        self.api_key = api_key
        self.trial = trial

    def __str__(self) -> str:
        return f"ID: {self.tg_id}. Completion: {self.completion}, total tokens: {self.total_tokens}, " \
               f"all time tokens: {self.all_time_tokens}, autotranslate_from = {self.auto_translate_from_user}" \
               f", autotranslate_to = {self.auto_translate_to_user}"
