from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import sqlite3
import datetime

TOKEN = '5165988091:AAGZ1qrF6r7f8cB_crlOzX0dpHltfViCyA8'
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
conn = sqlite3.connect('users.db')


@dp.message_handler(commands=['start'])
async def start(msg: types.Message):
    await msg.reply(
        "Привет, меня зовут HistoryBot, но для тебя Хисти. Готов тебя проконсультировать по некоторым историческим вопросам!")
    cur = conn.cursor()
    if not cur.execute(
            f'''SELECT * FROM users WHERE id = {msg.from_user.id}''').fetchall():
        sql = '''INSERT INTO users(id, username, name, regs) VALUES(?, ?, ?, ?)'''
        data_tuple = (
        msg.from_user.id, msg.from_user.username, msg.from_user.first_name, datetime.datetime.now().strftime("%Y-%m-%d"))
        cur.execute(sql, data_tuple)
        conn.commit()


@dp.message_handler(commands=['help'])
async def help(msg: types.Message):
    await msg.reply("Пока что команда в разработке")


# @dp.message_handler(commands=['search']):
# async def search(message: types.Message):
@dp.message_handler(commands=['view_dates'])
async def search(msg: types.Message):
    with open('dates.txt', 'r', encoding='utf-8') as file:
        info = file.readlines()
    for x in range(0, len('\n'.join(info)), 4096):
        await bot.send_message(msg.chat.id, '\n'.join(info)[x:x + 4096])


if __name__ == '__main__':
    executor.start_polling(dp)




