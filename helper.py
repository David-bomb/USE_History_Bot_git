import sqlite3
import json

from aiogram import types
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData


def datesDB_rewrite():  # Переписывание БД с датами
    conn = sqlite3.connect('dates.db')
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS dates( 
       date TEXT,
       event TEXT,
       event_lower TEXT
       )
    """)
    with open("dates.json", "r") as read_file:
        JsDates = json.load(read_file)
    # print(JsDates)
    sql = '''INSERT INTO dates(date, event, event_lower) VALUES(?, ?, ?)'''
    for i in JsDates.keys():
        data_tuple = (i, JsDates[i],  JsDates[i].lower())
        cur.execute(sql, data_tuple)
        conn.commit()
    print('Успешно переписана БД')




def usersDB_rewrite():
    # Этот файл нужен для переписывания базы данных пользователей в случае нужды
    conn = sqlite3.connect('users.db')
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS users( 
       id INT PRIMARY KEY,
       username TEXT,
       name TEXT,
       regs DATETIME)
    """)


def datesJS_rewrite():
    with open('dates.txt', encoding='utf-8') as file:
        info = file.readlines()
        # print(info)
    jsn = {}
    for i in info:
        i = ' ' + i.strip()
        # print(i)
        if i[1] != '#':
            # lol += 1
            # print(i.split(' – ')[1][-1], lol)
            jsn[i.split(' – ')[0]] = i.split(' – ')[1]
        # else:
        # jsn.append(i)
    # print(*txtDates)
    print(jsn)
    with open("dates.json", "w") as file:
        json.dump(jsn, file)
    '''with open("dates.json", "r") as read_file:
        JsDates = json.load(read_file)
    print(JsDates)'''


def datesTXTmoderniser():
    with open('dates.txt', encoding='utf-8') as file:
        info = file.readlines()
        info = list(map(lambda x: ' ' + x, info))
    with open('dates.txt', encoding='utf-8', mode='w') as file:
        file.write(''.join(info))


def unpacker(listt: list) -> list:
    spis = []
    for i in listt:
        spis.append(f'{i[0]} - {i[1]}')
    return spis
# datesJS_rewrite()
