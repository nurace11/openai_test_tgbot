import datetime

from sqlalchemy import Column, Integer, VARCHAR, TIMESTAMP, DATE

from .base import BaseModel


class User(BaseModel):
    __tablename__ = 'users_tg'

    def __init__(self, user_id, username):
        self.user_id = user_id
        self.username = username

    # Id
    user_id = Column(Integer, unique=True, nullable=False, primary_key=True)

    # username
    username = Column(VARCHAR(32), unique=False, nullable=True)

    # registered date
    reg_date = Column(TIMESTAMP, default=datetime.datetime.now())

    # last update date: check for new username
    upd_date = Column(DATE, default=datetime.date.today())

    # for debug

    def __str__(self):
        return f"<User: {self.user_id}, {self.username}, {self.reg_date}, {self.upd_date}"
