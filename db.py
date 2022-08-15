import sqlite3

# Этот файл нужен для переписывания базы данных пользователей в случае нужды
conn = sqlite3.connect('users.db')
cur = conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS users( 
   id INT PRIMARY KEY,
   username TEXT,
   name TEXT,
   regs DATETIME)
""")