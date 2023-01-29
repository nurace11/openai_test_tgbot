from database import sqlite_db
from entity.TgUser import TgUser
from openai import Completion

def find_all():
    return sqlite_db.cur.execute('SELECT * FROM tg_user').fetchall()


def find_user_by_id(user_id: int):
    try:
        userData = sqlite_db.cur.execute('SELECT * FROM tg_user WHERE id == ?', (user_id,)).fetchone()
        return TgUser(user_id, Completion(), '', userData[1], userData[2])
    except Exception as e:
        print(e)


def add_user(user: TgUser):
    sqlite_db.cur.execute('INSERT INTO tg_user VALUES(?, ?, ?)', (user.tg_id, user.total_tokens, user.all_time_tokens))
    sqlite_db.base.commit()


def update_user_by_id(user_id: int, user: TgUser):
    sqlite_db.cur.execute('UPDATE tg_user SET total_tokens == ?, all_time_tokens == ? WHERE id == ?',
                          (user.total_tokens, user.all_time_tokens, user_id))
    sqlite_db.base.commit()

# def delete_user_by_id(user_id: int):



