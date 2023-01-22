import sqlite3 as sq


def sql_start():
    global base, cur
    base = sq.connect('tg_openai_bot.db')
    cur = base.cursor()
    if base:
        print('Database connected OK')
    base.execute('CREATE TABLE IF NOT EXISTS menu('
                 'img TEXT, '
                 'name TEXT '
                 'PRIMARY KEY,'
                 'description TEXT,'
                 ' price TEXT)')
    base.commit()


async def sql_add_command(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO menu VALUES(?, ?, ?, ?)', tuple(data.values()))
        base.commit()


async def sql_read():
    return cur.execute('SELECT * FROM menu').fetchall()
