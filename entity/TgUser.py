import openai
from openai import Completion


class TgUser:
    def __init__(self, tg_id: int, completion=None, chat_history: str = None, total_tokens: int = 0,
                 all_time_tokens: int = 0):
        self.tg_id = tg_id
        self.completion = completion
        self.chat_history = chat_history
        self.total_tokens = total_tokens
        self.all_time_tokens = all_time_tokens

    def __str__(self) -> str:
        return f"ID: {self.tg_id}. Completion: {self.completion}, total tokens: {self.total_tokens}, " \
               f"all time tokens: {self.all_time_tokens}"
