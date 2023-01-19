FROM python:3.11

ADD bot_tg.py .

RUN pip install aiogram openai

CMD ["python", "./bot_tg.py"]