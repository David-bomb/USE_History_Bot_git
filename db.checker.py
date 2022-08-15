import sqlite3
conn = sqlite3.connect('users.db')
cur = conn.cursor()
print(cur.execute('''SELECT * FROM users''').fetchall())