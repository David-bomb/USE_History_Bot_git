from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import sqlite3
import datetime
import json
from helper import unpacker

# Создание бота
TOKEN = '5165988091:AAGZ1qrF6r7f8cB_crlOzX0dpHltfViCyA8'
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
# Создание соединений с файлами, вероятно перемещение их в отдельный файл
conn = sqlite3.connect('users.db')
cur = conn.cursor()
connection = sqlite3.connect('dates.db')
cursor = connection.cursor()
with open('dates.txt', 'r', encoding='utf-8') as file:
    txtDates = file.readlines()
with open("dates.json", "r") as read_file:
    JsDates = json.load(read_file)


@dp.message_handler(commands=['start'])  # Функция приветствия и регистрации
async def start(msg: types.Message):
    await msg.reply(
        "Привет, меня зовут HistoryBot, но для тебя Хисти. Готов тебя проконсультировать по некоторым историческим вопросам!")
    if not cur.execute(  # Регистрация юзера, если он еще не зарегистрирован
            f'''SELECT * FROM users WHERE id = {msg.from_user.id}''').fetchall():
        sql = '''INSERT INTO users(id, username, name, regs) VALUES(?, ?, ?, ?)'''
        data_tuple = (
            msg.from_user.id, msg.from_user.username, msg.from_user.first_name,
            datetime.datetime.now().strftime("%Y-%m-%d"))
        cur.execute(sql, data_tuple)
        conn.commit()


@dp.message_handler(commands=['help'])  # Команда помощь ¯\_(ツ)_/¯
async def help(msg: types.Message):
    await msg.reply("Пока что команда в разработке")


@dp.message_handler(commands=['view_dates'])
async def view(msg: types.Message):
    '''with open('dates.txt', 'r', encoding='utf-8') as file:
        txtDates = file.readlines()'''
    for x in range(0, len('\n'.join(txtDates)), 4096):
        await bot.send_message(msg.chat.id, '\n'.join(txtDates)[x:x + 4096], parse_mode='markdown')


@dp.message_handler(commands=['browse'])  # Первый прототип поиска по датам
async def search(msg: types.Message):
    '''with open("dates.json", "r") as read_file:
        JsDates = json.load(read_file)'''
    argument = msg.get_args()  # Получение даты
    # print(JsDates.keys())
    try:
        if argument.isdigit():
            if len(argument) == 3:  # TODO Доделать отсеивание лишних дат. ПРИМЕР: arg: 1945 , 1945 in ans
                date = cursor.execute(f''' SELECT * FROM dates WHERE date like '%{argument}%' ''').fetchall()
                if date:
                # print(date)
                    await bot.send_message(msg.chat.id, '\n'.join(unpacker(date)))
                else:
                    await msg.reply('Ничего не найдено!')
            elif len(argument) >= 4:
                date = cursor.execute(f''' SELECT * FROM dates WHERE date like '%{argument}%' ''').fetchall()
                if date:
                    await bot.send_message(msg.chat.id, '\n'.join(unpacker(date)))
                else:
                    await msg.reply('Ничего не найдено!')
            else:
                await msg.reply('Извините, я не могу обработать запрос короче 3-х символов.')
        else:
            await msg.reply('Пожалуйста, используйте цифры.')
    except:
        await msg.reply('Ошибка запроса! Попробуйте вписать запрос по шаблону!')


if __name__ == '__main__':
    executor.start_polling(dp)
