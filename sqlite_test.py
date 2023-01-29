import sqlite3

base = sqlite3.connect('nex.db')
cur = base.cursor()

print(type(base))
print(type(cur))

'''
text, integer, real, blob, null
'''

# base.execute('CREATE TABLE IF NOT EXISTS {}('.format('tg_users')
#              +
#              'id integer PRIMARY KEY,'
#              'password text'
#              ')')
# base.commit()

# CREATE
# cur.execute('INSERT INTO tg_users VALUES(?, ?)', (547852, 'qwert'))
# base.commit()

# cur.execute('INSERT INTO data VALUES(?, ?)', ('qwert', 'qwert'))
# base.commit()
#
# cur.execute('INSERT INTO data VALUES(?, ?)', ('re', 're'))
# base.commit()
#
# cur.executemany('INSERT INTO data VALUES(?, ?)', [['amogus', 'pass'], ['data', 'pass']])
# base.commit()


# READ
# fetchall = cur.execute('SELECT * FROM tg_users').fetchall()
# print(fetchall)
# ids = cur.execute('SELECT id FROM tg_users').fetchall()
# print(ids)
#
# r = cur.execute('SELECT password FROM tg_users WHERE id == ?', (123323,)).fetchone()
# print(r)


# UPDATE
cur.execute('UPDATE tg_users SET password == ? WHERE id == ?', ('passsword', 123323))
base.commit()

# DELETE
cur.execute('INSERT INTO tg_users VALUES(?, ?)', (999090, 'amogus'))
base.commit()
print('added new user')
print(cur.execute('SELECT * FROM tg_users WHERE id == ? ', (999090,)).fetchone())
cur.execute('DELETE FROM tg_users WHERE id == ?', (999090, ))
base.commit()
print('user deleted')
try:
    print(cur.execute('SELECT * FROM tg_users WHERE id == ? ', (999090,)).fetchone())
except Exception as e:
    print(e)


# DROP TABLE
execute = base.execute('DROP TABLE IF EXISTS data')
print(type(execute))


